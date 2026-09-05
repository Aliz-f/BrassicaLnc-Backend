#!/usr/bin/env python3
"""Deployment shortcuts; requires only Python 3 and Docker Compose on the host."""
import argparse
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'brassicaLncWeb'


def initialize(domain):
    if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?', domain):
        raise ValueError('Use an API hostname or IPv4 address, without scheme, port, or path.')
    if os.getuid() == 0:
        raise ValueError('Run init as the non-root deployment user, not with sudo.')
    values = {
        'SECRET_KEY': secrets.token_hex(32),
        'DATABASE_PASSWORD': secrets.token_hex(32),
        'DATABASE_USER': 'brassica',
        'APP_UID': str(os.getuid()),
        'APP_GID': str(os.getgid()),
        'ALLOWED_HOSTS': ','.join(dict.fromkeys([domain, 'localhost', '127.0.0.1'])),
        'CSRF_TRUSTED_ORIGINS': f'https://{domain},https://brassica.arfadaei.ir',
    }
    lines = (APP / '.env.example').read_text().splitlines()
    contents = '\n'.join(
        f'{line.split("=", 1)[0]}={values[line.split("=", 1)[0]]}'
        if line.split('=', 1)[0] in values else line for line in lines
    ) + '\n'
    # Exclusive creation preserves existing credentials, including on repeat runs.
    descriptor = os.open(APP / '.env', os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, 'w') as handle:
        handle.write(contents)
    for name in ('staticfiles', 'media'):
        (ROOT / 'deploy' / name).mkdir(mode=0o755, exist_ok=True)
    print('Created brassicaLncWeb/.env with random secrets and your UID/GID.')
    print('Review it, then run: python3 deploy/deploy.py up')


def compose(arguments):
    env_file = APP / '.env'
    if not env_file.is_file():
        raise ValueError('Missing brassicaLncWeb/.env. Run init API_HOSTNAME first.')
    # Make the file authoritative, avoiding stale exported credentials/ports.
    environment = os.environ.copy()
    for line in env_file.read_text().splitlines():
        match = re.match(r'^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=', line)
        if match:
            environment.pop(match.group(1), None)
    command = ['docker', 'compose', '--project-directory', str(APP),
               '--env-file', str(env_file), '-f', str(APP / 'docker-compose.yaml')]
    return subprocess.run(command + arguments, cwd=APP, env=environment).returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('init', help='Create .env without overwriting it').add_argument('domain')
    commands.add_parser('up', help='Build, start, and wait for readiness')
    commands.add_parser('status', help='Show service health and ports')
    commands.add_parser('logs', help='Follow recent application logs')
    commands.add_parser('check', help='Run Django deployment checks')
    args = parser.parse_args()
    try:
        if args.command == 'init':
            initialize(args.domain)
            return 0
        if args.command == 'up':
            result = compose(['config', '--quiet'])
            if result:
                return result
            result = compose(['up', '--build', '--wait', '--wait-timeout', '900'])
            if result:
                print('Deployment did not become healthy. Run: python3 deploy/deploy.py logs',
                      file=sys.stderr)
            return result
        return compose({
            'status': ['ps'],
            'logs': ['logs', '--follow', '--tail=100', 'web', 'database'],
            'check': ['exec', 'web', 'python', 'manage.py', 'check', '--deploy'],
        }[args.command])
    except (OSError, ValueError) as error:
        print(f'Deployment error: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
