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

#### Prerequisites

1. A running Dokploy instance
2. A custom domain configured (Dokploy handles SSL automatically via Let's Encrypt)

#### Deployment Steps

1. **Create a new Docker Compose application** in your Dokploy dashboard

2. **Connect your repository:**
   - Select this repository from GitHub/GitLab/Bitbucket
   - Or use the Git URL directly

3. **Configure environment variables** in Dokploy's Environment tab (use `.env.example` as reference):
   ```env
   # Required: Update these values
   SECRET_KEY=your-secret-key-here
   DJANGO_ALLOWED_HOSTS=.yourdomain.com
   CSRF_TRUSTED_ORIGINS=https://yourdomain.com

   # Email settings
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-password

   # Database (use defaults or customize)
   POSTGRES_USER=db_dictionary_user
   POSTGRES_PASSWORD=your-strong-password
   POSTGRES_DB=db_dictionary
   ```

4. **Configure your preferences** in `dictionary/apps.py`:
   - Update `DOMAIN` to your domain name
   - Update `PROTOCOL` to "https"
   - Update `FROM_EMAIL` to your email
   - Adjust other settings as needed

5. **Deploy:**
   - Click the "Deploy" button in Dokploy
   - The system will automatically:
     - Build all containers
     - Run database migrations
     - Collect static files
     - Create default users (anonymous & generic superuser)
     - Start all services

6. **Create an admin account:**
   - After successful deployment, access the web container console in Dokploy
   - Run: `python manage.py createsuperuser`
   - Or use Dokploy's terminal feature to execute commands

7. **Configure your domain:**
   - Add your domain in Dokploy's domain settings
   - SSL certificates will be automatically provisioned via Let's Encrypt

#### Features

✅ **Zero manual CLI commands** - Everything runs automatically on deployment
✅ **Automatic SSL/TLS** - Dokploy handles certificates via Let's Encrypt
✅ **Persistent storage** - All data (database, media, static) stored in Dokploy volumes
✅ **Auto-healing** - Containers restart automatically on failure
✅ **Easy updates** - Just push to your repository or click redeploy

#### Services Included

- **PostgreSQL** - Database
- **Redis** - Caching layer
- **RabbitMQ** - Message broker for Celery
- **Django/Gunicorn** - Web application
- **Celery Worker** - Background tasks
- **Celery Beat** - Scheduled tasks
- **Nginx** - Reverse proxy and static file serving

#### Notes

- The `docker-compose.yml` in the project root is specifically configured for Dokploy
- For traditional deployment, use the Makefile method described above
- All services communicate via Docker internal networking
- Volumes are stored in `../files/` relative to the docker-compose.yml (Dokploy standard)
