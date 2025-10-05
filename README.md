## django-sozluk, ekşi sözlük clone powered by Python

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](LICENSE)

Demo website is now available at [sozluk.me](https://sozluk.me/) \
Check [CHANGELOG](CHANGELOG) before cloning a newer version!

This is a clone of ekşi sözlük. Commonly referred as "collaborative
dictionary", this type of social networking can be thought as "urban dictionary
on steroids". Visit
[this Wikipedia article](https://en.wikipedia.org/wiki/Ek%C5%9Fi_S%C3%B6zl%C3%BCk)
to learn more about this type of social network.

**This project is currently maintained.** If you want to contribute to the
project or have found a bug or need help about deployment
etc., [create an issue](https://github.com/realsuayip/django-sozluk/issues/new).

Check out [screenshots](screenshots) folder to see current front-end in action
with both the desktop and mobile views.

### Deployment Guide

#### Requirements

1. Have Docker, with Compose plugin (v2) installed in your system.
2. Have GNU make installed in your system.
3. Have your SSL certificates and dhparam file under `docker/prod/nginx/certs`.
   They should be named exactly as following: `server.crt`, `server.key`
   and `dhparam.pem`
4. Change and configure secrets in `django.env` and `postgres.env` files
   under `conf/prod`
5. Configure your preferences in `dictionary/apps.py`

#### Deployment

> [!IMPORTANT]
> When running any `make` command make sure `CONTEXT` environment variable is
> set to `production`

**In the project directory, run this command:**

```shell
CONTEXT=production make
```

At this point, your server will start serving requests via https port (443).
You should see a 'server error' page when you navigate to your website.

**To complete the installation, you need to run a initialization script:**

```shell
CONTEXT=production make setup
```

After running this command, you should be able to navigate through your website
without any issues. At this point, you should create an administrator account
to log in and manage your website:

```shell
CONTEXT=production make run createsuperuser
```

### Dokploy Deployment Guide

This project is fully compatible with [Dokploy](https://dokploy.com/) - a self-hosted Platform as a Service (PaaS) alternative to Heroku, Vercel, and Netlify.

#### What Changed from Original Repository

To enable seamless Dokploy deployment, the following modifications were made:

**New Files Created:**
- `docker-compose.yml` - Unified compose file with all 7 services (db, redis, rabbitmq, web, nginx, celery-worker, celery-beat)
- `docker/prod/django/entrypoint.sh` - Automated initialization script (migrations, static files, superuser creation)
- `docker/prod/nginx/Dockerfile.dokploy` - Nginx container for Dokploy deployment
- `docker/prod/nginx/nginx.conf.dokploy` - Nginx main configuration (HTTP-only, Traefik handles SSL)
- `docker/prod/nginx/sites-enabled/dokploy.conf` - Nginx site configuration with upstream backend
- `.env.example` - Comprehensive environment variables reference

**Modified Files:**
- `docker/prod/django/prod.Dockerfile` - Added `AS builder` alias, `su-exec` package, removed `USER django` directive
- `.dockerignore` - Changed to only exclude `docker/dev` (was excluding entire `docker/` directory)
- `docker/prod/django/prod.Dockerfile.dockerignore` - Changed to only exclude `docker/dev`

**Key Architectural Changes:**
- Uses external `dokploy-network` for all services (required by Dokploy)
- No custom container names (Dokploy auto-names for logs/metrics integration)
- Volume paths use `../files/` pattern (Dokploy standard)
- Nginx listens on HTTP only (port 80) - Traefik handles SSL termination
- Entrypoint runs as root initially to fix volume permissions, then switches to `django` user
- All initialization is automated and idempotent (safe to run multiple times)

#### Prerequisites

1. A running Dokploy instance
2. A domain name configured with Dokploy (SSL automatically provisioned via Let's Encrypt)

#### Deployment Steps

1. **Create a new Docker Compose application** in your Dokploy dashboard

2. **Connect your repository:**
   - Select this repository from GitHub/GitLab/Bitbucket
   - Or use the Git URL directly
   - Branch: `master`

3. **Configure environment variables** in Dokploy's Environment tab:

   **Required (Django Core):**
   ```env
   SECRET_KEY=your-secret-key-here-change-this-to-a-random-string-min-50-chars
   DJANGO_ALLOWED_HOSTS=.yourdomain.com yourdomain.com localhost
   CSRF_TRUSTED_ORIGINS=https://yourdomain.com
   ```

   > ⚠️ **IMPORTANT**: `DJANGO_ALLOWED_HOSTS` must be **space-separated**, not comma-separated!
   > Django splits this value by spaces. Example: `.yourdomain.com yourdomain.com localhost`

   **Required (Email):**
   ```env
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-email-password
   ```

   **Optional (Database - uses defaults if not set):**
   ```env
   POSTGRES_USER=db_dictionary_user
   POSTGRES_PASSWORD=db_dictionary_password
   POSTGRES_DB=db_dictionary
   SQL_USER=db_dictionary_user
   SQL_PASSWORD=db_dictionary_password
   SQL_DATABASE=db_dictionary
   ```

   **Optional (Automatic Superuser Creation):**
   ```env
   DJANGO_SUPERUSER_USERNAME=admin
   DJANGO_SUPERUSER_EMAIL=admin@yourdomain.com
   DJANGO_SUPERUSER_PASSWORD=change-this-secure-password
   ```

   > 💡 If these variables are set, a superuser will be automatically created on first deployment.
   > The script is idempotent - it won't create duplicates on subsequent deployments.

   **Optional (Redis & RabbitMQ - uses defaults if not set):**
   ```env
   REDIS_URL=redis://redis:6379/
   RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
   ```

   **Optional (Session & Cache):**
   ```env
   SESSION_ENGINE=dictionary.backends.sessions.cached_db
   EMAIL_BACKEND=djcelery_email.backends.CeleryEmailBackend
   ```

   See `.env.example` file for complete reference.

4. **Configure your preferences** in `dictionary/apps.py`:
   - Update `DOMAIN` to your domain name
   - Update `PROTOCOL` to "https"
   - Update `FROM_EMAIL` to your email
   - Adjust other settings as needed

5. **Deploy:**
   - Click the "Deploy" button in Dokploy
   - The entrypoint script will automatically:
     - Wait for PostgreSQL to be ready
     - Run database migrations
     - Collect static files
     - Create default users (anonymous & generic author)
     - Create superuser (if ENV variables are set)
     - Fix volume permissions
     - Start the application
   - All services will start with health checks and proper dependencies

6. **Configure your domain:**
   - Add your domain in Dokploy's Domains settings
   - SSL certificates will be automatically provisioned via Let's Encrypt
   - Traefik (Dokploy's reverse proxy) handles all HTTPS/SSL termination

7. **Access your site:**
   - Navigate to your domain
   - Log in with your superuser credentials (if auto-created) or create one manually

#### Features

✅ **Zero manual CLI commands** - Everything runs automatically on deployment
✅ **Automatic SSL/TLS** - Dokploy handles certificates via Let's Encrypt
✅ **Persistent storage** - All data (database, media, static) stored in Dokploy volumes
✅ **Auto-healing** - Containers restart automatically on failure
✅ **Easy updates** - Just push to your repository or click redeploy
✅ **Automatic superuser creation** - Set ENV variables for one-click admin account
✅ **Idempotent deployments** - Safe to redeploy multiple times
✅ **Integrated logging** - All logs accessible via Dokploy UI

#### Services Architecture

The deployment includes 7 containerized services:

- **db** (PostgreSQL 17.6) - Main database with health checks
- **redis** (Redis 8.2) - Caching layer and session storage
- **rabbitmq** (RabbitMQ 4.1) - Message broker for Celery tasks
- **web** (Django 5.2 + Gunicorn) - Main application with 4 workers
- **celery-worker** - Processes background tasks asynchronously
- **celery-beat** - Handles scheduled periodic tasks
- **nginx** - Reverse proxy and static file server

All services communicate via the `dokploy-network` and have proper health checks and startup dependencies.

#### Troubleshooting

**400 Bad Request Error:**
- Check that `DJANGO_ALLOWED_HOSTS` is **space-separated**, not comma-separated
- Example: `DJANGO_ALLOWED_HOSTS=.yourdomain.com yourdomain.com localhost`
- Include both the wildcard subdomain (`.yourdomain.com`) and the root domain

**Containers not appearing in Dokploy Terminal:**
- Ensure no custom `container_name` directives are set (already fixed in docker-compose.yml)
- Verify all services are on `dokploy-network`

**Permission Errors on Volumes:**
- The entrypoint script automatically fixes permissions on `/app/static` and `/app/media`
- Containers run as root initially, fix permissions, then switch to `django` user

**Database Connection Issues:**
- Check that database credentials match in all services (web, celery-worker, celery-beat)
- Ensure `SQL_HOST=db` (service name, not container name)
- Verify PostgreSQL health check is passing before web starts

**Static Files Not Loading:**
- Nginx serves static files from `/app/static` volume
- Entrypoint runs `collectstatic --noinput` automatically on deployment
- Check nginx logs: `dokploy logs -f <app-name> --service nginx`

**RabbitMQ Connection Issues:**
- Ensure `RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/`
- RabbitMQ takes ~10-15 seconds to become healthy on first start
- Check health status in Dokploy dashboard

**Viewing Logs:**
Use the `dokploy` CLI or Dokploy UI:
```bash
dokploy logs -f <app-name> --service web
dokploy logs -f <app-name> --service db
dokploy logs -f <app-name> --service nginx
```

#### Notes

- The `docker-compose.yml` in the project root is specifically configured for Dokploy
- For traditional deployment, use the Makefile method described in the first section
- All services communicate via Docker internal networking (service names as hostnames)
- Volumes are stored in `../files/` relative to the docker-compose.yml (Dokploy standard)
- Nginx only handles HTTP (port 80) - Traefik (Dokploy's reverse proxy) handles HTTPS/SSL
- Superuser creation is optional but recommended for easier first-time setup
- The deployment uses pinned Docker image SHA256 hashes for reproducibility
