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

### Traditional Deployment Guide (with Makefile)

This deployment method uses Docker Compose with manual SSL certificate management.

#### Requirements

1. Have Docker, with Compose plugin (v2) installed in your system.
2. Have your SSL certificates and dhparam file under `docker/prod/nginx/certs`.
   They should be named exactly as following: `server.crt`, `server.key`
   and `dhparam.pem`
3. Configure environment variables in `.env` file (see `.env.example`)

#### Deployment

**Option 1: Automatic Deployment (Recommended)**

Create a `.env` file with your configuration (see `.env.example`), then run:

```shell
docker compose up -d --build
```

The entrypoint script will automatically:
- Run database migrations
- Collect static files
- Create default users (via quicksetup)
- Create superuser (if ENV variables are set)
- Start all services

**Option 2: Manual Deployment (Legacy)**

> [!NOTE]
> This method is kept for backwards compatibility. The automatic method above is recommended.

Set the `CONTEXT` environment variable to `production` when running make commands:

```shell
# 1. Start all services
CONTEXT=production make

# 2. Run initialization (migrations, static files, default users)
CONTEXT=production make setup

# 3. Create superuser manually
CONTEXT=production make run createsuperuser
```

#### Configuration

All configuration is done via environment variables in your `.env` file:

**Required:**
```env
SECRET_KEY=your-secret-key-min-50-chars
DJANGO_ALLOWED_HOSTS=.yourdomain.com yourdomain.com localhost
CSRF_TRUSTED_ORIGINS=https://yourdomain.com
APP_DOMAIN=yourdomain.com
APP_PROTOCOL=https
APP_FROM_EMAIL=noreply@yourdomain.com
POSTGRES_PASSWORD=secure-password
SQL_PASSWORD=secure-password
```

**Optional (for automatic superuser creation):**
```env
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@yourdomain.com
DJANGO_SUPERUSER_PASSWORD=secure-password
```

See `.env.example` for all available environment variables and their descriptions.

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

   All configuration is done via environment variables - no manual file editing required!

   **Required Variables:**
   ```env
   # Django Core
   SECRET_KEY=your-secret-key-here-min-50-chars
   DJANGO_ALLOWED_HOSTS=.yourdomain.com yourdomain.com localhost 127.0.0.1
   CSRF_TRUSTED_ORIGINS=https://yourdomain.com

   # Application Settings
   APP_DOMAIN=yourdomain.com
   APP_PROTOCOL=https
   APP_FROM_EMAIL=noreply@yourdomain.com

   # Database
   POSTGRES_USER=db_dictionary_user
   POSTGRES_PASSWORD=secure-password-here
   POSTGRES_DB=db_dictionary
   SQL_USER=db_dictionary_user
   SQL_PASSWORD=secure-password-here
   SQL_DATABASE=db_dictionary
   ```

   > ⚠️ **IMPORTANT**: `DJANGO_ALLOWED_HOSTS` must be **space-separated**, not comma-separated!
   > Example: `.yourdomain.com yourdomain.com localhost`

   **Optional Variables:**
   ```env
   # Email (leave empty to disable email functionality)
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-specific-password

   # Automatic Superuser Creation
   DJANGO_SUPERUSER_USERNAME=admin
   DJANGO_SUPERUSER_EMAIL=admin@yourdomain.com
   DJANGO_SUPERUSER_PASSWORD=secure-admin-password

   # Redis & RabbitMQ (defaults work for most cases)
   REDIS_URL=redis://redis:6379/
   RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/

   # Debug mode (0=off, 1=on - keep 0 for production)
   DEBUG=0
   ```

   **All Environment Variables:**

   | Variable | Required | Default | Description |
   |----------|----------|---------|-------------|
   | `SECRET_KEY` | ✅ Yes | - | Django secret key (min 50 chars) |
   | `DJANGO_ALLOWED_HOSTS` | ✅ Yes | - | Space-separated domains Django will serve |
   | `CSRF_TRUSTED_ORIGINS` | ✅ Yes | - | Trusted origins for CSRF (with https://) |
   | `APP_DOMAIN` | ✅ Yes | - | Primary domain (used in emails/URLs) |
   | `APP_PROTOCOL` | ❌ No | `https` | Protocol (http or https) |
   | `APP_FROM_EMAIL` | ✅ Yes | - | From address for outgoing emails |
   | `POSTGRES_USER` | ✅ Yes | - | PostgreSQL username |
   | `POSTGRES_PASSWORD` | ✅ Yes | - | PostgreSQL password |
   | `POSTGRES_DB` | ✅ Yes | - | PostgreSQL database name |
   | `SQL_USER` | ✅ Yes | - | Django database user (must match POSTGRES_USER) |
   | `SQL_PASSWORD` | ✅ Yes | - | Django database password (must match POSTGRES_PASSWORD) |
   | `SQL_DATABASE` | ✅ Yes | - | Django database name (must match POSTGRES_DB) |
   | `EMAIL_HOST` | ❌ No | - | SMTP server hostname |
   | `EMAIL_PORT` | ❌ No | `587` | SMTP server port |
   | `EMAIL_HOST_USER` | ❌ No | - | SMTP username |
   | `EMAIL_HOST_PASSWORD` | ❌ No | - | SMTP password |
   | `DJANGO_SUPERUSER_USERNAME` | ❌ No | - | Auto-create admin username |
   | `DJANGO_SUPERUSER_EMAIL` | ❌ No | - | Auto-create admin email |
   | `DJANGO_SUPERUSER_PASSWORD` | ❌ No | - | Auto-create admin password |
   | `REDIS_URL` | ❌ No | `redis://redis:6379/` | Redis connection URL |
   | `RABBITMQ_URL` | ❌ No | `amqp://guest:guest@rabbitmq:5672/` | RabbitMQ connection URL |
   | `DEBUG` | ❌ No | `0` | Debug mode (0=off, 1=on) |
   | `SQL_ENGINE` | ❌ No | `django.db.backends.postgresql` | Django database backend |
   | `SQL_HOST` | ❌ No | `db` | Database host |
   | `SQL_PORT` | ❌ No | `5432` | Database port |
   | `SESSION_ENGINE` | ❌ No | `dictionary.backends.sessions.cached_db` | Session backend |
   | `EMAIL_BACKEND` | ❌ No | `djcelery_email.backends.CeleryEmailBackend` | Email backend |

   **How to Generate SECRET_KEY:**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

   See `.env.example` file for detailed descriptions of each variable.

4. **Deploy:**
   - Click the "Deploy" button in Dokploy
   - The entrypoint script will automatically:
     - Wait for PostgreSQL to be ready
     - Run database migrations (`python manage.py migrate`)
     - Collect static files (`python manage.py collectstatic`)
     - Create default users via quicksetup (`python manage.py quicksetup`)
     - Create superuser if ENV variables are set (`python manage.py createsuperuser`)
     - Fix volume permissions
     - Start the application with Gunicorn
   - All services will start with health checks and proper dependencies
   - **No manual commands required!**

5. **Configure your domain:**
   - Add your domain in Dokploy's Domains settings
   - SSL certificates will be automatically provisioned via Let's Encrypt
   - Traefik (Dokploy's reverse proxy) handles all HTTPS/SSL termination

6. **Access your site:**
   - Navigate to your domain
   - Log in with your superuser credentials (if auto-created)
   - Everything is ready to use!

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
