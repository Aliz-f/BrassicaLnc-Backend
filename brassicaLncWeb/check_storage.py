"""Check bind-mount access before migrations or static-file collection."""
import os
from pathlib import Path
import sys


def check_storage(root):
    def require_access(path, mode):
        if not os.access(path, mode):
            raise PermissionError(f'Insufficient access to {path}')

    for name in ('staticfiles', 'media'):
        directory = root / name
        if not directory.is_dir():
            raise PermissionError(f'Missing directory: {directory}')
        require_access(directory, os.R_OK | os.W_OK | os.X_OK)

    def walk_error(error):
        raise error

    # Old root-owned directories may sit below a writable mount root.
    # WhiteNoise also reads and rewrites existing compressed static files.
    for directory, _, filenames in os.walk(root / 'staticfiles', onerror=walk_error):
        require_access(directory, os.R_OK | os.W_OK | os.X_OK)
        for filename in filenames:
            require_access(Path(directory) / filename, os.R_OK | os.W_OK)


if __name__ == '__main__':
    try:
        check_storage(Path(__file__).resolve().parent)
    except OSError as error:
        print(f'Storage preflight failed (UID={os.getuid()}, GID={os.getgid()}): {error}. '
              'Repair ownership and permissions recursively on the host deploy/staticfiles '
              'directory; see README: Repair existing static-file permissions.', file=sys.stderr)
        sys.exit(1)
