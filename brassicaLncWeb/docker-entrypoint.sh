#!/bin/sh

set -eu

cd /app/brassicaLncWeb

python manage.py migrate --noinput

if [ "${SEED_DATABASE:-true}" = "true" ]; then
    python manage.py seed_database
fi

python manage.py shell -c "from blast_rest import utils; from blast_rest.views import blastn; print('blast_rest import smoke check passed'); print(utils.__name__); print(blastn.__name__)"

blastn -version >/dev/null

python manage.py collectstatic --noinput

exec "$@"
