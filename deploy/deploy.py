#!/usr/bin/env python3
"""Deployment shortcuts; requires only Python 3 and Docker Compose on the host."""
import argparse
import json
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
    uid = os.getuid() or 1000
    gid = os.getgid() if os.getuid() != 0 else 1000
    values = {
        'SECRET_KEY': secrets.token_hex(32),
        'DATABASE_PASSWORD': secrets.token_hex(32),
        'DATABASE_USER': 'brassica',
        'APP_UID': str(uid),
        'APP_GID': str(gid),
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
    print(f'Created brassicaLncWeb/.env with random secrets and container UID/GID {uid}:{gid}.')
    print('Review it, then run: python3 deploy/deploy.py up')


def compose(arguments, capture_output=False):
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
    result = subprocess.run(command + arguments, cwd=APP, env=environment,
                            capture_output=capture_output, text=True)
    return result if capture_output else result.returncode


def repair_permissions():
    if os.getuid() != 0:
        raise ValueError('Run fix-permissions as root (or with sudo) to change host ownership.')
    result = compose(['config', '--format', 'json'], capture_output=True)
    if result.returncode:
        raise ValueError('Compose configuration is invalid; run up to see validation errors.')
    arguments = json.loads(result.stdout)['services']['web']['build']['args']
    uid, gid = int(arguments['APP_UID']), int(arguments['APP_GID'])
    if uid <= 0 or gid <= 0:
        raise ValueError('Set APP_UID and APP_GID to positive IDs (1000 recommended for root deployments).')
    for name in ('staticfiles', 'media'):
        base = ROOT / 'deploy' / name
        if base.is_symlink():
            raise ValueError(f'Refusing to change ownership through symlink: {base}')
        base.mkdir(mode=0o755, exist_ok=True)
        def fail(error):
            raise error
        for directory, directories, filenames in os.walk(base, onerror=fail):
            for path in [Path(directory)] + [Path(directory) / item for item in filenames]:
                if path.is_symlink():
                    continue
                os.chown(path, uid, gid)
                # Static assets are public; preserve existing media visibility.
                access = (0o755 if path.is_dir() else 0o644) if name == 'staticfiles' else (
                    0o700 if path.is_dir() else 0o600)
                path.chmod((path.stat().st_mode & 0o777) | access)
    print(f'Repaired staticfiles/media ownership for container UID/GID {uid}:{gid}.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('init', help='Create .env without overwriting it').add_argument('domain')
    commands.add_parser('up', help='Build, start, and wait for readiness')
    commands.add_parser('status', help='Show service health and ports')
    commands.add_parser('logs', help='Follow recent application logs')
    commands.add_parser('check', help='Run Django deployment checks')
    commands.add_parser('fix-permissions', help='Repair host static/media ownership as root')
    args = parser.parse_args()
    try:
        if args.command == 'init':
            initialize(args.domain)
            return 0
        if args.command == 'fix-permissions':
            repair_permissions()
            return 0
        if args.command == 'up':
            result = compose(['config', '--quiet'])
            if result:
                return result
            if os.getuid() == 0:
                result = compose(['build', 'web'])
                if result:
                    return result
                result = compose(['stop', 'web'])
                if result:
                    return result
                repair_permissions()
                result = compose(['up', '--no-build', '--wait', '--wait-timeout', '900'])
            else:
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
