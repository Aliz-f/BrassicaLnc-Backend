#!/bin/sh

set -eu

cd /app/brassicaLncWeb

# Check nested static directories too: the mount root alone may be writable.
python check_storage.py

python manage.py check
python manage.py migrate --noinput

case "$(printf '%s' "${SEED_DATABASE:-true}" | tr '[:upper:]' '[:lower:]')" in
    true|1|yes|on) python manage.py seed_database ;;
    false|0|no|off) ;;
    *) echo 'SEED_DATABASE must be true or false.' >&2; exit 1 ;;
esac

python manage.py shell -c "from blast_rest import utils; from blast_rest.views import blastn; print('blast_rest import smoke check passed'); print(utils.__name__); print(blastn.__name__)"

blastn -version >/dev/null

python manage.py collectstatic --noinput

exec "$@"
