# BrassicaLnc Backend

Django REST API, admin, reference-data downloads, and nucleotide BLAST for BrassicaLnc. This repository does not contain the frontend; `/` returning 404 is expected. Use `/search/id/` or `/admin/login/` to verify the backend.

## Project structure

| Path | Purpose |
| --- | --- |
| `brassicaLncWeb/brassicaLncWeb/` | Django settings, routes, WSGI/ASGI |
| `brassicaLncWeb/{lncRNA,search,download,submit,statistic}/` | API apps; schema migrations are version controlled |
| `brassicaLncWeb/files/` | Runtime download and expression datasets; keep in the image |
| `brassicaLncWeb/data_initialization/*.json` | Bundled reference fixtures for first deployment |
| `brassicaLncWeb/blast_rest/` | Bundled BLAST REST code |
| `brassicaLncWeb/blast_rest/data/db/` | Prebuilt nucleotide BLAST database |
| `brassicaLncWeb/Dockerfile`, `docker-compose.yaml` | Python 3.11/Gunicorn and PostgreSQL 17 services |
| `deploy/nginx/brassicaLnc.conf.example` | Host nginx reverse proxy configuration |
| `deploy/staticfiles/`, `deploy/media/` | Persistent host directories shared with the app |
| `requirements` | Pinned runtime dependencies |

The deployment uses **host nginx → localhost Gunicorn container → private PostgreSQL container**. There is no nginx container or active `brassicaLncWeb/nginx/default.conf`. The legacy root `blast_rest` gitlink has no submodule configuration and is not used by the image; the required runtime is now a normal tracked package inside the Django project. The REST API is available at both `/blast/blastn` and `/blast/blastn/`; legacy django-blastplus HTML forms are no longer exposed because their Biopython imports are incompatible with modern versions.

## Step-by-step server deployment

These commands assume an Ubuntu server, a sudo-capable deployment user, and a checkout at `/srv/brassicaLnc-back`. The frontend is hosted on GitHub Pages at `https://brassica.arfadaei.ir`. Replace `api.example.com` with the separate domain you assign to the backend server. Keep the same checkout path and Compose project name across upgrades so PostgreSQL uses the same volume.

### 1. Install server prerequisites

Install Docker Engine and the Compose plugin using the [official Ubuntu instructions](https://docs.docker.com/engine/install/ubuntu/). Do not mix Ubuntu's `docker.io` packages with Docker's own package repository. Verify Docker access before continuing:

```bash
docker --version
docker compose version
docker info
sudo apt update
sudo apt install -y git nginx openssl certbot python3-certbot-nginx
sudo systemctl enable --now docker nginx
```

If Docker requires sudo, use `sudo docker` consistently below, or configure access using Docker's installation guide. Allow SSH and TCP 80/443 through the server/cloud firewall; PostgreSQL has no published port and the application port stays on loopback. Point the domain's DNS A record (and AAAA only if IPv6 is configured) to this server.

### 2. Clone the repository

```bash
sudo install -d -o "$(id -un)" -g "$(id -gn)" /srv/brassicaLnc-back
git clone https://github.com/Aliz-f/BrassicaLnc-Backend.git /srv/brassicaLnc-back
cd /srv/brassicaLnc-back
cp brassicaLncWeb/.env.example brassicaLncWeb/.env
chmod 600 brassicaLncWeb/.env
```

Deploy a commit containing the migration files and deployment changes. The fixtures, runtime files, and BLAST database must also be present in the checkout.

### 3. Configure environment and directory permissions

Generate two different random values, one for `SECRET_KEY` and one for `DATABASE_PASSWORD`:

```bash
openssl rand -hex 32
openssl rand -hex 32
id -u
id -g
nano brassicaLncWeb/.env
```

Set these values (no spaces around `=`):

```dotenv
SECRET_KEY=<first-generated-value>
DATABASE_PASSWORD=<second-generated-value>
DATABASE_NAME=brassica
DATABASE_USER=brassica
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_HOST=database
DATABASE_PORT=5432
DEBUG=False
ALLOWED_HOSTS=api.example.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://brassica.arfadaei.ir
CSRF_TRUSTED_ORIGINS=https://api.example.com,https://brassica.arfadaei.ir
APP_PORT=8000
APP_UID=1000
APP_GID=1000
SEED_DATABASE=true
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
```

Use your actual non-root deployment user's numeric UID/GID from `id` for `APP_UID`/`APP_GID`. Hosts have no scheme or path; CORS/CSRF origins include their scheme and any nonstandard port. Keep the secret stable across restarts. The app refuses a missing, placeholder, or shorter-than-50-character production secret.

```bash
mkdir -p deploy/staticfiles deploy/media
sudo chown -R "$(id -u):$(id -g)" deploy/staticfiles deploy/media
chmod 755 deploy deploy/staticfiles deploy/media
```

The bind-mounted directories must be writable by the UID/GID configured above and readable/traversable by nginx. Image permissions do not override host bind-mount permissions. Do not use `chmod 777`.

### 4. Build and start

Run all subsequent Compose commands from this directory:

```bash
cd /srv/brassicaLnc-back/brassicaLncWeb
docker compose --env-file .env config --quiet
docker compose --env-file .env up -d --build
docker compose --env-file .env logs -f web
```

Using `--env-file .env` explicitly supplies both Compose interpolation (ports, credentials, build arguments) and the application's environment. See [Docker's interpolation documentation](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/). Avoid sharing expanded `docker compose config` output because it contains secrets.

Startup waits for PostgreSQL, applies migrations, imports all reference fixtures in one transaction if all fixture-backed reference tables are empty, verifies BLAST imports/binary, collects static files, and starts one Gunicorn worker with a 120-second timeout. The initial import can take several minutes. Ctrl+C exits log following without stopping the services.

Subsequent starts skip import when every fixture-backed reference table has data. A partially populated dataset causes a clear startup error instead of silently serving incomplete data. Restore a complete backup or investigate it; use `SEED_DATABASE=false` only for an intentionally managed dataset. Existing partially populated databases from the older startup script cannot be repaired automatically. Do not run the legacy initialization script on production data.

### 5. Verify the application

```bash
docker compose --env-file .env ps
curl -f http://127.0.0.1:8000/search/id/
curl -I http://127.0.0.1:8000/admin/login/
docker compose --env-file .env exec web python manage.py check
docker compose --env-file .env exec web blastn -version
docker compose --env-file .env exec web python manage.py createsuperuser
```

`ps` should show only `127.0.0.1:8000` published for web (or your chosen port). `/search/id/` should return JSON with a nonzero count. The app and database restart automatically after a server reboot when Docker is enabled.

### 6. Configure host nginx

```bash
sudo cp ../deploy/nginx/brassicaLnc.conf.example /etc/nginx/sites-available/brassicaLnc.conf
sudo nano /etc/nginx/sites-available/brassicaLnc.conf
```

Set `server_name` to your API domain, adjust both alias paths if you used a different checkout location, and change the `proxy_pass` port if `APP_PORT` differs from 8000. For IPv6, add `listen [::]:80;`. The example forwards the original host and HTTPS scheme and allows enough time for BLAST responses.

```bash
sudo ln -s /etc/nginx/sites-available/brassicaLnc.conf /etc/nginx/sites-enabled/brassicaLnc.conf
sudo nginx -t
sudo systemctl reload nginx
curl -f http://api.example.com/search/id/
```

Skip the symlink command if it already exists. For an IP-only installation, use the server IP as `server_name` and include it in `ALLOWED_HOSTS`. Do not enter admin credentials over public plain HTTP.

### 7. Enable HTTPS

With DNS resolving correctly and port 80 reachable:

```bash
sudo certbot --nginx -d api.example.com
sudo certbot renew --dry-run
curl -f https://api.example.com/search/id/
```

Choose HTTP-to-HTTPS redirection. Then edit `.env`:

```dotenv
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=3600
```

```bash
docker compose --env-file .env up -d web
docker compose --env-file .env exec web python manage.py check --deploy
```

Review any warnings. HSTS starts at one hour; increase it only after HTTPS is stable. Subdomain HSTS and preload are intentionally not enabled. nginx must keep overwriting `X-Forwarded-Proto` with `$scheme`; the application trusts that header. After HTTPS redirection is enabled, use the public HTTPS URL for curl checks. Configure the GitHub Pages frontend at `https://brassica.arfadaei.ir` to use your backend HTTPS API origin. Keep the frontend domain pointing to GitHub Pages; point only the separate API domain to this server. An HTTPS frontend requires an HTTPS API to avoid browser mixed-content blocking. `ALLOWED_HOSTS` must contain the API hostname, while `CORS_ALLOWED_ORIGINS` contains the frontend origin.

## Updates, backups, and restore

Before every upgrade, take a database backup and preserve `.env` and `deploy/media` securely off-server. From `brassicaLncWeb/`:

```bash
mkdir -p ../backups
chmod 700 ../backups
umask 077
docker compose --env-file .env exec -T database sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > "../backups/brassica-$(date +%Y%m%d-%H%M%S).dump"
```

Check that the command succeeds; a nonempty file alone is not proof of a valid backup. Test restoration on a separate environment. Changing `DATABASE_PASSWORD` in `.env` does not change an existing PostgreSQL role's password; rotate it in PostgreSQL too. Do not change the PostgreSQL major version against the same data volume without a database upgrade plan.

```bash
git pull --ff-only
docker compose --env-file .env up -d --build
docker compose --env-file .env logs --tail=100 web
curl -f https://api.example.com/search/id/
```

For restoration into a **new, empty database volume**, set `SEED_DATABASE=false`, start only `database`, and restore the backup before starting web:

```bash
docker compose --env-file .env up -d database
# Wait until database is healthy in `docker compose --env-file .env ps`.
docker compose --env-file .env exec -T database sh -c 'pg_restore --exit-on-error --no-owner --no-privileges -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < ../backups/your-backup.dump
docker compose --env-file .env up -d web
```

Restore media separately and verify the API/admin. Do not restore over a running application or populated database. `docker compose down` preserves the database; **`docker compose down -v` deletes it**. Rolling application code back may also require restoring the matching database backup if migrations changed the schema.

## Troubleshooting and limitations

- **400 / DisallowedHost:** correct `ALLOWED_HOSTS` and recreate web with `up -d web`.
- **502:** inspect web logs; initial seeding may still be running, or nginx may target the wrong port.
- **Static files return 403:** check directory ownership and nginx traversal permissions on every parent directory.
- **CSRF / CORS errors:** check exact frontend origins, HTTPS scheme forwarding, and recreate web after environment changes.
- **Missing tables:** ensure the three apps' migration directories were committed. For an existing manually created schema, inspect it before considering `migrate --fake-initial`; never blindly fake migrations.
- **Submission email:** records are saved, but the legacy mail helper has no configured recipient and reports `email: false`. Use the admin to review submissions; notification delivery needs separate configuration/code changes.
- **BLAST:** uses the bundled nucleotide database and a pinned Biopython version that still provides the deprecated command wrappers. Load-test with representative sequences before increasing Gunicorn workers; each BLAST request consumes server CPU and memory. Legacy protein/HTML routes are not part of this deployment.
- **Scope:** Django was upgraded to the [supported 5.2 LTS series](https://www.djangoproject.com/download/). Deployment checks are not an exhaustive scientific-output or application-security audit. Keep dependencies patched and validate your frontend workflows before switching production traffic.

For local Python development, install `requirements`, install the system `ncbi-blast+` package, run commands from `brassicaLncWeb/`. Set `DEBUG=True` for development; absent database settings use SQLite. Do not use Django's development server in production.

## Validation performed

The deployment changes were checked with an image build, fresh PostgreSQL migrations and import (17,946 fixture records), repeat seeding, search responses (1,854 transcripts), admin/static HTTP responses, and successful nucleotide BLAST queries. Three regression tests cover REST routing, partial-dataset protection, and import rollback. `check --deploy` with HTTPS settings reports only the intentionally disabled HSTS subdomain/preload options. Server-specific DNS, TLS certificates, nginx permissions, and frontend integration must be verified on your server.
