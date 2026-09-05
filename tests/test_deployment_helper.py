import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('deployment', ROOT / 'deploy/deploy.py')
deployment = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deployment)


class DeploymentHelperTests(unittest.TestCase):
    def test_root_init_uses_nonroot_container_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            app = root / 'brassicaLncWeb'
            app.mkdir()
            (root / 'deploy').mkdir()
            (app / '.env.example').write_text((ROOT / 'brassicaLncWeb/.env.example').read_text())
            with patch.object(deployment, 'ROOT', root), patch.object(deployment, 'APP', app), \
                    patch.object(os, 'getuid', return_value=0), \
                    patch.object(os, 'getgid', return_value=0):
                deployment.initialize('api.example.com')
            contents = (app / '.env').read_text()
            self.assertIn('APP_UID=1000\n', contents)
            self.assertIn('APP_GID=1000\n', contents)

    def test_root_repairs_nested_assets_without_following_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            nested = root / 'deploy/staticfiles/admin/css'
            nested.mkdir(parents=True)
            asset = nested / 'responsive_rtl.css'
            asset.write_text('body {}')
            asset.chmod(0o400)
            external = root / 'external'
            external.write_text('preserve')
            external.chmod(0o600)
            (nested / 'link').symlink_to(external)
            with patch.object(deployment, 'ROOT', root), \
                    patch.object(os, 'getuid', return_value=0), \
                    patch.object(os, 'chown') as chown, \
                    patch.object(deployment, 'compose') as compose:
                compose.return_value.returncode = 0
                compose.return_value.stdout = json.dumps({'services': {'web': {
                    'build': {'args': {'APP_UID': '1000', 'APP_GID': '1001'}}}}})
                deployment.repair_permissions()
                chown.assert_any_call(asset, 1000, 1001)
                self.assertNotIn(external, [call.args[0] for call in chown.call_args_list])
                self.assertNotIn(nested / 'link', [call.args[0] for call in chown.call_args_list])
            self.assertEqual(asset.stat().st_mode & 0o777, 0o644)
            self.assertEqual(external.stat().st_mode & 0o777, 0o600)

    def test_root_up_builds_and_stops_web_before_repair(self):
        actions = []
        with patch.object(os, 'getuid', return_value=0), \
                patch.object(deployment.sys, 'argv', ['deploy.py', 'up']), \
                patch.object(deployment, 'compose',
                             side_effect=lambda args: actions.append(args) or 0), \
                patch.object(deployment, 'repair_permissions',
                             side_effect=lambda: actions.append('repair')):
            self.assertEqual(deployment.main(), 0)
        self.assertEqual(actions, [
            ['config', '--quiet'], ['build', 'web'], ['stop', 'web'], 'repair',
            ['up', '--no-build', '--wait', '--wait-timeout', '900']])

    def test_init_generates_private_config_and_preserves_it_on_repeat(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            app = root / 'brassicaLncWeb'
            app.mkdir()
            (root / 'deploy').mkdir()
            (app / '.env.example').write_text((ROOT / 'brassicaLncWeb/.env.example').read_text())
            with patch.object(deployment, 'ROOT', root), patch.object(deployment, 'APP', app), \
                    patch.object(os, 'getuid', return_value=1234), \
                    patch.object(os, 'getgid', return_value=1235):
                deployment.initialize('api.example.com')
                original = (app / '.env').read_text()
                with self.assertRaises(FileExistsError):
                    deployment.initialize('another.example.com')
                self.assertEqual((app / '.env').read_text(), original)
            values = dict(line.split('=', 1) for line in original.splitlines()
                          if line and not line.startswith('#'))
            self.assertEqual(len(values['SECRET_KEY']), 64)
            self.assertNotEqual(values['SECRET_KEY'], values['DATABASE_PASSWORD'])
            self.assertEqual(values['APP_UID'], '1234')
            self.assertEqual((app / '.env').stat().st_mode & 0o777, 0o600)
            self.assertTrue((root / 'deploy/media').is_dir())

    def test_compose_uses_file_settings_from_any_working_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            app = Path(directory)
            (app / '.env').write_text('DATABASE_PASSWORD=file-secret\nAPP_PORT=8000\n')
            with patch.object(deployment, 'APP', app), \
                    patch.dict(os.environ, DATABASE_PASSWORD='stale', APP_PORT='9000'), \
                    patch.object(deployment.subprocess, 'run') as run:
                run.return_value.returncode = 0
                self.assertEqual(deployment.compose(['config', '--quiet']), 0)
                self.assertNotIn('DATABASE_PASSWORD', run.call_args.kwargs['env'])
                self.assertNotIn('APP_PORT', run.call_args.kwargs['env'])
                self.assertEqual(run.call_args.kwargs['cwd'], app)
