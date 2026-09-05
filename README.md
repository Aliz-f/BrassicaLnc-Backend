# BrassicaLnc Backend

Django REST API, admin, reference-data downloads, and nucleotide BLAST. The frontend is a separate project hosted at `[https://brassica.arfadaei.ir](https://brassica.arfadaei.ir)`. Deploy this backend on its own hostname, such as `api.example.com`; keep the frontend domain pointing to GitHub Pages.

Deployment: **host nginx → localhost Gunicorn container → private PostgreSQL 17 container**. Reference fixtures and the nucleotide BLAST database are bundled in the image. `/` returns 404 by design; use `/healthz/`, `/search/id/`, or `/admin/login/`.

## 1. Prepare the server

The instructions below assume Ubuntu, a **root shell**, and a checkout at `/srv/brassicaLnc-back`. Root runs Docker and manages host files; the application container still runs as UID/GID `1000:1000`. For a non-root deployment user, prefix administrative commands with `sudo`; the helper uses that user’s IDs instead.

Install Docker Engine and its Compose plugin using the [official Ubuntu instructions](https://docs.docker.com/engine/install/ubuntu/). Verify that your deployment user can run Docker:

```bash
docker --version
docker compose version
docker info
apt update
apt install -y git python3 nginx certbot python3-certbot-nginx
systemctl enable --now docker nginx

```

Configure Docker access following its installation guide if `docker info` fails. The helper below invokes Docker as your current user. It requires a Compose version supporting `up --wait --wait-timeout` ([Compose reference](https://docs.docker.com/reference/cli/docker/compose/up/)).

Point your **API hostname's** DNS A record at this server. Add an AAAA record only if IPv6 works. Allow SSH and TCP 80/443 through your server/cloud firewall. The application binds to loopback; PostgreSQL has no published port.

## 2. Clone and generate configuration

```bash
install -d -o "$(id -un)" -g "$(id -gn)" /srv/brassicaLnc-back
git clone https://github.com/Aliz-f/BrassicaLnc-Backend.git /srv/brassicaLnc-back
cd /srv/brassicaLnc-back
python3 deploy/deploy.py init api.example.com
nano brassicaLncWeb/.env

```

Replace `api.example.com` with your API hostname. Run `init` from your root shell. It generates separate random Django/database secrets, sets container UID/GID to `1000:1000` for root deployments (or your IDs for non-root deployments), creates the static/media directories, and writes `.env` with mode 600. **It refuses to overwrite an existing `.env`.** For an existing installation, keep your current file and review it against `.env.example`; do not regenerate database credentials.

Review these settings:

| Setting                                               | Value / purpose                                                                                                |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `ALLOWED_HOSTS`                                       | API hostname, `localhost`, `127.0.0.1`; no scheme or path                                                      |
| `CORS_ALLOWED_ORIGINS`                                | Frontend origins, including scheme; defaults to `[https://brassica.arfadaei.ir](https://brassica.arfadaei.ir)` |
| `CSRF_TRUSTED_ORIGINS`                                | API and frontend HTTPS origins                                                                                 |
| `APP_PORT`                                            | Loopback port used by nginx; defaults to `8000`                                                                |
| `APP_UID`, `APP_GID`                                  | Container IDs; use `1000` for both when running deployment as root, never `0`                                  |
| `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD` | Shared directly between Django web service and PostgreSQL database                                             |
| `SECRET_KEY`                                          | Stable random secret, at least 50 characters                                                                   |
| `SEED_DATABASE`                                       | `true` to import bundled reference data on first startup                                                       |

Compose loads environment values directly from `.env` via `env_file`. Production constants (such as `DATABASE_HOST=database`, `DATABASE_PORT=5432`, and `DATABASE_ENGINE=django.db.backends.postgresql`) are pre-configured directly inside `docker-compose.yml`. Keep HTTPS cookie/redirect settings disabled until step 6. Use single quotes around manually chosen secrets containing literal `$` or `#`. Never commit or share `.env` or expanded `docker compose config` output.

For an existing root-operated installation, preserve your secrets and set these values in `brassicaLncWeb/.env`:

```dotenv
APP_UID=1000
APP_GID=1000

```

Do not use root's `id -u` / `id -g` values (`0`) for the container. Running `python3 deploy/deploy.py up` as root now builds the image, stops web, recursively repairs static/media ownership to the configured container IDs, and starts the services. This repairs files left by earlier deployments automatically. It does not change database-volume ownership. Changing container IDs requires a rebuild, which `up` includes.

For manual repair as root, stop web first and run `python3 deploy/deploy.py fix-permissions`, then `up`. Repair skips symlinks, grants public read access to static assets, and preserves existing media visibility while granting the application owner access. Non-root users can run this repair command with `sudo` if old files belong to another user.

Keep the checkout under `/srv`, as shown. A checkout inside `/root` normally prevents host nginx from reading static/media files because it cannot traverse `/root`.

## 3. Build and start

From the repository root:

```bash
python3 deploy/deploy.py up
python3 deploy/deploy.py status

```

The helper validates Compose configuration, builds the image, repairs host permissions when run as root, and waits up to 15 minutes for both services to become healthy. Initial seeding may take several minutes. Startup checks directory access and Django configuration, applies migrations, imports reference fixtures atomically, checks BLAST imports/binary, collects static files, and starts Gunicorn.

The database service uses a streamlined health check running PostgreSQL CLI commands over local Unix socket connections (`psql -U ... -c "SELECT 1"`). The web health check requests `/healthz/` through Gunicorn via `healthcheck.py` and executes a database query. It also works after HTTPS redirects are enabled. Health checks have a ten-minute initial grace period for seeding; health status alone does not restart an unhealthy running container. The restart policy handles exited containers and server reboots.

On failure:

```bash
python3 deploy/deploy.py logs

```

Ctrl+C stops following logs without stopping the services. A timeout leaves containers available for diagnosis. Inspect logs before retrying `up`.

The helper finds configuration relative to its own location, so it can be invoked from any directory using its absolute path. For settings declared in `.env`, it ignores exported shell overrides. Keep the same checkout location and Compose project name across upgrades to retain the same database volume.

Equivalent manual commands, from `brassicaLncWeb/`:

```bash
docker compose --env-file .env config --quiet
docker compose --env-file .env up --build --wait --wait-timeout 900

```

Manual Compose commands let exported shell variables override `.env`; both services resolve database credentials consistently. See [Docker's interpolation rules](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/).

## 4. Verify and create an administrator

```bash
curl -f http://127.0.0.1:8000/healthz/
curl -f http://127.0.0.1:8000/search/id/
curl -I http://127.0.0.1:8000/admin/login/
cd brassicaLncWeb
docker compose --env-file .env exec web python manage.py createsuperuser
docker compose --env-file .env exec web blastn -version
cd ..

```

Use your chosen `APP_PORT` if different. Health should return `{"status": "ok"}`, search should return a nonzero count, and admin should return HTTP 200. The default fixture set contains 1,854 transcripts.

Later startups skip seeding when all fixture-backed tables contain data. A partially populated dataset stops startup instead of silently serving incomplete data. Restore a complete backup or investigate it. Set `SEED_DATABASE=false` only when intentionally managing the dataset yourself. Do not run the legacy initialization scripts against production data.

## 5. Configure nginx

```bash
cp deploy/nginx/brassicaLnc.conf.example /etc/nginx/sites-available/brassicaLnc.conf
nano /etc/nginx/sites-available/brassicaLnc.conf

```

Set `server_name` to your API hostname. Update both alias paths if your checkout is elsewhere, and `proxy_pass` if `APP_PORT` is not 8000. Add `listen [::]:80;` if using IPv6.

```bash
ln -s /etc/nginx/sites-available/brassicaLnc.conf /etc/nginx/sites-enabled/brassicaLnc.conf
nginx -t
systemctl reload nginx
curl -f http://api.example.com/healthz/

```

Skip the symlink command if it already exists. nginx needs traversal permission on every parent of the static/media paths. Do not enter administrator credentials over public plain HTTP.

## 6. Enable HTTPS and connect the frontend

Once DNS resolves and port 80 is reachable:

```bash
certbot --nginx -d api.example.com
certbot renew --dry-run
curl -f https://api.example.com/healthz/

```

Choose HTTP-to-HTTPS redirection. Edit `brassicaLncWeb/.env`:

```dotenv
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=3600

```

Apply and check:

```bash
python3 deploy/deploy.py up
python3 deploy/deploy.py check
curl -f https://api.example.com/search/id/

```

Review [Django deployment checks](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/). HSTS starts at one hour; increase it after HTTPS is stable. Subdomain HSTS and preload are not enabled by default. nginx must overwrite `X-Forwarded-Proto` with `$scheme`, as the example does, because Django trusts that header. Use public HTTPS URLs for manual checks after enabling redirects.

Configure the separate frontend to use `[https://api.example.com](https://api.example.com)` as its API origin. An HTTPS frontend needs an HTTPS API. Verify browser searches, downloads, and BLAST; CORS origins must match the frontend exactly.

## Updates and backups

Back up before every upgrade. Preserve `.env` and `deploy/media` securely off-server. From `brassicaLncWeb/`:

```bash
mkdir -p ../backups
chmod 700 ../backups
umask 077
docker compose --env-file .env exec -T database sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > "../backups/brassica-$(date +%Y%m%d-%H%M%S).dump"

```

Check the command's exit status and test restoration separately; a nonempty file is insufficient. Then, from the repository root:

```bash
git pull --ff-only
python3 deploy/deploy.py up
python3 deploy/deploy.py status
curl -f https://api.example.com/healthz/

```

Changes to environment settings require container recreation (`up`); `restart` alone does not apply them. Changing `DATABASE_PASSWORD` does not rotate a stored PostgreSQL password. Do not change PostgreSQL's major version against the same volume without a database upgrade plan.

### Restore to a new, empty database volume

Set `SEED_DATABASE=false`. From `brassicaLncWeb/`, start only PostgreSQL and wait for it to become healthy:

```bash
docker compose --env-file .env up --wait --wait-timeout 120 database
docker compose --env-file .env exec -T database sh -c 'pg_restore --exit-on-error --no-owner --no-privileges -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < ../backups/your-backup.dump
cd ..
python3 deploy/deploy.py up

```

Restore media separately. Do not restore over a populated database or a running application. `docker compose down` preserves data; **`docker compose down -v` deletes database volumes**. Rolling back application code may require a matching database backup if migrations changed the schema.

## Troubleshooting

| Symptom                                    | Action                                                                                        |
| ------------------------------------------ | --------------------------------------------------------------------------------------------- |
| `init` reports an existing file            | Keep `.env`; compare it with `.env.example` and edit as needed                                |
| Cannot write staticfiles/media             | Fix host ownership to match `APP_UID`/`APP_GID` (`1000:1000`), then rebuild if IDs changed    |
| Database unhealthy / authentication failed | Check for an existing volume with older credentials; use the procedure below                  |
| Web unhealthy / readiness timeout          | Inspect `python3 deploy/deploy.py logs`; check migrations, seed errors, and mount permissions |
| 400 / DisallowedHost                       | Correct API hostname in `ALLOWED_HOSTS`, then run `up`                                        |
| 502                                        | Check web health/logs and nginx's loopback port                                               |
| Static files return 403                    | Check nginx traversal/read permissions on the entire alias path                               |
| CSRF / CORS errors                         | Check exact origins and nginx HTTPS forwarding; recreate web                                  |
| Missing tables                             | Verify tracked migrations are present; do not blindly fake migrations                         |

### Repair existing static-file permissions

`PermissionError` during `collectstatic` (for example, `admin/css/responsive_rtl.css`) means the application cannot replace an existing asset. A writable `staticfiles` root does not guarantee writable nested directories. This can happen after a previous deployment ran as root or with a different UID/GID. Startup now checks nested static directories and existing files before running migrations.

From the server checkout's `brassicaLncWeb/` directory, stop web and obtain the actual image user's IDs, then repair the host bind mount:

```bash
docker compose --env-file .env stop web
static_uid=$(docker compose --env-file .env run --rm --no-deps --entrypoint id web -u)
static_gid=$(docker compose --env-file .env run --rm --no-deps --entrypoint id web -g)
chown -R "$static_uid:$static_gid" ../deploy/staticfiles
chmod -R u+rwX,go+rX ../deploy/staticfiles
docker compose --env-file .env up --wait --wait-timeout 900 web

```

These commands bypass normal startup when inspecting the user, so they also work during a restart loop. They preserve static files and database data. If you subsequently change `APP_UID`/`APP_GID`, rebuild first and repeat the repair with the new image's IDs. If the preflight instead names `media`, fix that directory's ownership/access for the same user. Do not use `chmod 777` or delete the database volume.

### Existing database password mismatch

Retain the database volume. Connect using the administrator role originally used to initialize it (the helper uses `DATABASE_USER`, defaulting to `brassica`):

```bash
cd brassicaLncWeb
docker compose --env-file .env exec database psql -U brassica -d brassica

```

At the psql prompt, run `\password brassica`, enter the exact `.env` password twice without surrounding quotes, then `\q`. Substitute the original role/database if different. Rebuilding an image does not change stored credentials. Verify independently of the normal startup script:

```bash
docker compose --env-file .env run --rm --no-deps --entrypoint python web manage.py shell -c "from django.db import connection; connection.ensure_connection(); print('Database connection OK')"
cd ..
python3 deploy/deploy.py up

```

## Development and project layout

- `brassicaLncWeb/brassicaLncWeb/`: Django settings, routes, readiness endpoint, WSGI/ASGI.
- `brassicaLncWeb/{lncRNA,search,download,submit,statistic}/`: API apps and tracked migrations.
- `brassicaLncWeb/files/`, `data_initialization/*.json`: runtime datasets and initial fixtures; required in the image.
- `brassicaLncWeb/blast_rest/`: bundled BLAST API and prebuilt database. The legacy root `blast_rest` gitlink is not used by Docker.
- `deploy/deploy.py`: host setup and deployment helper; uses Python's standard library.
- `deploy/nginx/`, `deploy/staticfiles/`, `deploy/media/`: host proxy configuration and persistent files.
- `requirements`: pinned Python dependencies used by the image.

For local development, use a fresh Python 3.11 virtual environment, install `requirements` and the system `ncbi-blast+` package, and run Django commands from `brassicaLncWeb/`. Set `DEBUG=True`; absent database engine settings use SQLite. An existing `.env` still supplies database settings. Do not use Django's development server in production.

Run host helper/Compose tests (Compose CLI required, no daemon needed):

```bash
python3 -m unittest discover -s tests -v

```

Run application regression tests in the built image with an isolated in-memory SQLite database:

```bash
cd brassicaLncWeb
docker compose --env-file .env run --rm --no-deps -e DATABASE_ENGINE= --entrypoint python web manage.py test lncRNA

```

Submission records are saved, but the legacy email helper has no configured recipient and reports `email: false`; review submissions in admin. BLAST REST accepts `/blast/blastn` and `/blast/blastn/`. Legacy HTML/protein routes are not exposed. Biopython is pinned to retain the command wrappers; load-test representative queries before increasing the default single Gunicorn worker.

Deployment verification covers image build, fresh PostgreSQL migration/seeding, readiness with HTTPS settings, repeat seeding, and regression tests. DNS, certificates, host nginx permissions, and the separate frontend must be verified on your target server.
