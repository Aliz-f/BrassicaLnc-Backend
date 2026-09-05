import importlib.util
import os
from pathlib import Path
import tempfile
import unittest


spec = importlib.util.spec_from_file_location(
    'check_storage', Path(__file__).resolve().parents[1] / 'brassicaLncWeb/check_storage.py')
storage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(storage)


@unittest.skipIf(os.getuid() == 0, 'Root bypasses normal filesystem permissions')
class StoragePermissionsTests(unittest.TestCase):
    def test_nested_directory_permissions_are_checked_and_repair_passes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            nested = root / 'staticfiles/admin/css'
            nested.mkdir(parents=True)
            (root / 'media').mkdir()
            (nested / 'responsive_rtl.css').write_text('body {}')
            nested.chmod(0o555)
            try:
                self.assertTrue(os.access(root / 'staticfiles', os.W_OK))
                with self.assertRaisesRegex(PermissionError, 'admin/css'):
                    storage.check_storage(root)
            finally:
                nested.chmod(0o755)
            storage.check_storage(root)

    def test_readonly_existing_static_file_is_detected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'staticfiles').mkdir()
            (root / 'media').mkdir()
            asset = root / 'staticfiles/asset.css.gz'
            asset.write_bytes(b'existing')
            asset.chmod(0o444)
            try:
                with self.assertRaisesRegex(PermissionError, 'asset.css.gz'):
                    storage.check_storage(root)
            finally:
                asset.chmod(0o644)
