# BrassicaLnc Backend

Backend services for the BrassicaLnc website.

The main deployable Django project lives in [brassicaLncWeb/](brassicaLncWeb/) and serves the API, admin site, and the data download endpoints. The repository also contains a local BLAST REST package in [blast_rest/](blast_rest/) that is installed from source during image builds.

## Project Layout

- [brassicaLncWeb/](brassicaLncWeb/) - main Django project and application code.
- [brassicaLncWeb/files/](brassicaLncWeb/files/) - runtime reference data used by download endpoints.
- [brassicaLncWeb/data_initialization/](brassicaLncWeb/data_initialization/) - database bootstrap data.
- [blast_rest/](blast_rest/) - local package required by the main Python dependencies.
- [requirements](requirements) - pinned Python dependencies used by the Docker image and local installs.

## Docker Deployment

The repository is containerized with two services:

- `web` - Django + Gunicorn
- `database` - PostgreSQL 17

The Django container runs migrations, seeds initial data when the database is empty, smoke-checks the BLAST package, collects static assets, and then starts Gunicorn. The service publishes on `127.0.0.1:${APP_PORT}` so the VM's own nginx can reverse proxy to it.

### Prerequisites

- Docker Engine
- Docker Compose v2
- nginx installed on the VM host
- a domain name pointed at the VM if you want HTTPS
- optional: certbot or another ACME client for SSL certificates

### Environment

The app reads settings from [brassicaLncWeb/.env.example](brassicaLncWeb/.env.example).

For a real deployment, create [brassicaLncWeb/.env](brassicaLncWeb/.env) with production values. At minimum, set:

- `SECRET_KEY`
- `DATABASE_PASSWORD`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`

Also set `APP_PORT`, `APP_UID`, and `APP_GID` if you want the container to match your host deployment layout. The defaults work on a typical Linux VM, but you can align them with the user and group that own your deployment directory.

### Run Locally with Docker

From the repository root:

```bash
docker compose -f brassicaLncWeb/docker-compose.yaml up --build
```

The app will be available at:

- http://127.0.0.1:8000

### Deploy on a VM

This is the recommended production flow when nginx is installed on the VM host and Docker is only used for the app and database.

1. Install prerequisites on the VM.

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin nginx
sudo systemctl enable --now docker nginx
```

2. Clone the repository onto the VM.

```bash
git clone git@github.com:Aliz-f/BrassicaLnc-Backend.git /srv/brassicaLnc-back
cd /srv/brassicaLnc-back
```

3. Create the deployment folders that nginx and Django will share.

```bash
mkdir -p deploy/staticfiles deploy/media
```

4. Copy the environment template and fill in production values.

```bash
cp brassicaLncWeb/.env.example brassicaLncWeb/.env
```

Edit `brassicaLncWeb/.env` and set at least `SECRET_KEY`, `DATABASE_PASSWORD`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and `APP_PORT`.

5. If needed, adjust ownership of the deployment directories so the Docker container can write collected static files.

```bash
sudo chown -R $USER:$USER deploy
```

If you want the container UID/GID to match the host deployment user, set `APP_UID` and `APP_GID` in `brassicaLncWeb/.env`.

6. Start the Docker stack.

```bash
docker compose -f brassicaLncWeb/docker-compose.yaml up -d --build
```

7. Confirm that the web container is bound to localhost only.

```bash
docker compose -f brassicaLncWeb/docker-compose.yaml ps
```

You should see `127.0.0.1:8000->8000/tcp` or the port you set in `APP_PORT`.

8. Review the startup logs.

```bash
docker compose -f brassicaLncWeb/docker-compose.yaml logs -f web
```

The first startup should run migrations, load the initial data, verify `blast_rest`, run `blastn -version`, and collect static files.

9. Install the host nginx site configuration.

Copy the example file from [deploy/nginx/brassicaLnc.conf.example](deploy/nginx/brassicaLnc.conf.example) to `/etc/nginx/sites-available/brassicaLnc.conf` and update:

- `server_name` to your domain
- the `alias` paths if your repository is stored somewhere else
- the `proxy_pass` port if you changed `APP_PORT`

10. Enable the nginx site and reload nginx.

```bash
sudo ln -s /etc/nginx/sites-available/brassicaLnc.conf /etc/nginx/sites-enabled/brassicaLnc.conf
sudo nginx -t
sudo systemctl reload nginx
```

11. Open the public site through nginx.

Point your browser to `http://your-domain/` or `http://your-vm-ip/`.

12. Add HTTPS.

Use certbot or your preferred ACME client to issue a certificate for the domain, then keep nginx on the host terminating TLS and forwarding traffic to `127.0.0.1:${APP_PORT}`.

### What Starts Automatically

On the first startup the web container will:

1. Run Django migrations.
2. Check whether `lncRNA.Lnc` already has rows.
3. If the database is empty, run [brassicaLncWeb/data_initialization/initial_database.py](brassicaLncWeb/data_initialization/initial_database.py) from the data directory so the bundled JSON fixtures are loaded.
4. Smoke-check `blast_rest` imports and the `blastn` binary.
5. Collect static assets into the host-mounted `deploy/staticfiles` directory.
6. Start Gunicorn on the localhost-published port.

If you remove the PostgreSQL volume, the next startup will seed the data again.

## Useful Commands

Run Django management commands inside the web container:

```bash
docker compose -f brassicaLncWeb/docker-compose.yaml exec web python manage.py createsuperuser
docker compose -f brassicaLncWeb/docker-compose.yaml exec web python manage.py test
docker compose -f brassicaLncWeb/docker-compose.yaml exec web blastn -version
```

Run the BLAST REST smoke check inside the container:

```bash
docker compose -f brassicaLncWeb/docker-compose.yaml exec web python - <<'PY'
from blast_rest import utils
from blast_rest.views import blastn
print('blast_rest import smoke check passed')
print(utils.__name__)
print(blastn.__name__)
PY
```

## Publishing With Host Nginx

The VM's nginx should live outside Docker and proxy HTTP/HTTPS traffic to the Django container on `127.0.0.1:${APP_PORT}`. It should also serve static and media files from the host directories mounted into the container.

Recommended production steps:

1. Create a DNS `A` record for your domain or point your VM IP at the server.
2. Install nginx on the VM host, outside Docker.
3. Start this stack with `docker compose -f brassicaLncWeb/docker-compose.yaml up -d --build`.
4. Add a host nginx site config that proxies to `127.0.0.1:${APP_PORT}` and serves `/static/` and `/media/` from the repo's `deploy/` directories.
5. Enable the site and reload nginx.
6. Add SSL with certbot or your certificate provider, then keep Docker private on localhost.

A sample host nginx config is in [deploy/nginx/brassicaLnc.conf.example](deploy/nginx/brassicaLnc.conf.example).

Example host nginx flow:

```nginx
server {
	listen 80;
	server_name your-domain.example;

	location /static/ {
		alias /srv/brassicaLnc-back/deploy/staticfiles/;
	}

	location /media/ {
		alias /srv/brassicaLnc-back/deploy/media/;
	}

	location / {
		proxy_pass http://127.0.0.1:8000;
		proxy_set_header Host $host;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Forwarded-Proto $scheme;
	}
}
```

If you use certbot, the HTTPS server block should keep the same `location /`, `location /static/`, and `location /media/` rules and only add the TLS certificate directives and an HTTP-to-HTTPS redirect.

## Notes

- The project uses PostgreSQL in Docker, but the Django settings fall back to SQLite when no database environment variables are present.
- The download views read files from the project `files/` directory, so those files must remain inside the image or mounted into the container.
- The repository includes a legacy standalone BLAST package in [blast_rest/](blast_rest/); it is installed automatically because the main dependency list references it by local path.
