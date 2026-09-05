"""Run with python3 -m unittest discover -s tests (Compose CLI required)."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

COMPOSE = Path(__file__).resolve().parents[1] / 'brassicaLncWeb/docker-compose.yaml'


class ComposeCredentialsTests(unittest.TestCase):
    def render(self, overrides=None, password='file_password'):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'compose.yaml').write_text(COMPOSE.read_text())
            (root / '.env').write_text(
                "DATABASE_USER=file_user\nDATABASE_NAME=file_database\n"
                f"DATABASE_PASSWORD='{password}'\n"
                "SECRET_KEY=test-only\nALLOWED_HOSTS=localhost\n"
            )
            env = {key: value for key, value in os.environ.items()
                   if not key.startswith(('DATABASE_', 'COMPOSE_'))}
            env.update(overrides or {})
            result = subprocess.run(
                ['docker', 'compose', '--env-file', str(root / '.env'),
                 '-f', str(root / 'compose.yaml'), 'config', '--format', 'json'],
                env=env, capture_output=True, text=True, check=True,
            )
            return json.loads(result.stdout)['services']

    def assert_credentials_match(self, services):
        web = services['web']['environment']
        database = services['database']['environment']
        for app_key, db_key in [('DATABASE_USER', 'POSTGRES_USER'),
                               ('DATABASE_PASSWORD', 'POSTGRES_PASSWORD'),
                               ('DATABASE_NAME', 'POSTGRES_DB')]:
            self.assertEqual(web[app_key], database[db_key])

    def test_file_credentials_match(self):
        self.assert_credentials_match(self.render())

    def test_shell_overrides_cannot_split_credentials(self):
        services = self.render({'DATABASE_USER': 'shell_user',
                                'DATABASE_PASSWORD': 'shell_password',
                                'DATABASE_NAME': 'shell_database'})
        self.assert_credentials_match(services)
        self.assertEqual(services['web']['environment']['DATABASE_PASSWORD'],
                         'shell_password')

    def test_quoted_special_characters_survive(self):
        password = 'test$UNSET_VARIABLE#value with spaces'
        services = self.render(password=password)
        self.assert_credentials_match(services)
        # Compose config escapes literal dollars for reusable YAML/JSON output.
        rendered = services['web']['environment']['DATABASE_PASSWORD']
        self.assertEqual(rendered.replace('$$', '$'), password)


if __name__ == '__main__':
    unittest.main()
