#!/bin/sh

set -eu

cd /app/brassicaLncWeb

python manage.py migrate --noinput

if ! python manage.py shell -c "from lncRNA.models import Lnc; import sys; sys.exit(0 if Lnc.objects.exists() else 1)"; then
    cd /app/brassicaLncWeb/data_initialization
    python initial_database.py
    cd /app/brassicaLncWeb
fi

python manage.py shell -c "from blast_rest import utils; from blast_rest.views import blastn; print('blast_rest import smoke check passed'); print(utils.__name__); print(blastn.__name__)"

blastn -version >/dev/null

python manage.py collectstatic --noinput

exec "$@"