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

---

## Other Deployment Methods

For traditional deployment methods (Docker Compose with Makefile, manual setup, etc.), please refer to the [original repository](https://github.com/realsuayip/django-sozluk).

---

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

---

# Türkçe (Turkish)

## django-sozluk, Python ile geliştirilmiş ekşi sözlük klonu

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](LICENSE)

Demo sitesi [sozluk.me](https://sozluk.me/) adresinden erişilebilir

Bu proje ekşi sözlük'ün bir klonudur. "İşbirlikçi sözlük" olarak adlandırılan bu sosyal ağ türü, "steroidli urban dictionary" olarak düşünülebilir. Bu sosyal ağ türü hakkında daha fazla bilgi için [bu Wikipedia makalesini](https://tr.wikipedia.org/wiki/Ek%C5%9Fi_S%C3%B6zl%C3%BCk) ziyaret edebilirsiniz.

**Bu proje aktif olarak geliştirilmektedir.** Projeye katkıda bulunmak istiyorsanız, bir hata bulduysanız veya deployment konusunda yardıma ihtiyacınız varsa, [bir issue oluşturun](https://github.com/realsuayip/django-sozluk/issues/new).

Mevcut arayüzü masaüstü ve mobil görünümleriyle görmek için [screenshots](screenshots) klasörüne göz atın.

---

## Diğer Deployment Yöntemleri

Geleneksel deployment yöntemleri (Makefile ile Docker Compose, manuel kurulum vb.) için lütfen [orijinal repoya](https://github.com/realsuayip/django-sozluk) bakın.

---

### Dokploy Deployment Rehberi

Bu proje [Dokploy](https://dokploy.com/) ile tamamen uyumludur - Heroku, Vercel ve Netlify'a self-hosted alternatif bir Platform as a Service (PaaS) çözümü.

#### Orijinal Repodan Yapılan Değişiklikler

Sorunsuz Dokploy deployment'ı sağlamak için aşağıdaki değişiklikler yapılmıştır:

**Oluşturulan Yeni Dosyalar:**
- `docker-compose.yml` - 7 servisi içeren birleşik compose dosyası (db, redis, rabbitmq, web, nginx, celery-worker, celery-beat)
- `docker/prod/django/entrypoint.sh` - Otomatik başlatma scripti (migration'lar, statik dosyalar, superuser oluşturma)
- `docker/prod/nginx/Dockerfile.dokploy` - Dokploy deployment için Nginx container'ı
- `docker/prod/nginx/nginx.conf.dokploy` - Nginx ana yapılandırması (yalnızca HTTP, Traefik SSL yönetir)
- `docker/prod/nginx/sites-enabled/dokploy.conf` - Upstream backend ile Nginx site yapılandırması
- `.env.example` - Kapsamlı environment variable referansı

**Değiştirilen Dosyalar:**
- `docker/prod/django/prod.Dockerfile` - `AS builder` alias eklendi, `su-exec` paketi eklendi, `USER django` direktifi kaldırıldı
- `.dockerignore` - Yalnızca `docker/dev` hariç tutulacak şekilde değiştirildi (tüm `docker/` dizini hariç tutuluyordu)
- `dictionary/apps.py` - Environment variable'lardan okuma desteği eklendi (manuel düzenleme gereksiz)

**Temel Mimari Değişiklikler:**
- Tüm servisler için harici `dokploy-network` kullanılır (Dokploy tarafından gereklidir)
- Özel container isimleri yok (Dokploy log/metrik entegrasyonu için otomatik isimlendirme)
- Volume yolları `../files/` pattern'i kullanır (Dokploy standardı)
- Nginx yalnızca HTTP dinler (port 80) - Traefik SSL termination'ı yönetir
- Entrypoint önce root olarak çalışır, volume izinlerini düzeltir, sonra `django` kullanıcısına geçer
- Tüm başlatma otomatik ve idempotent'tir (birden fazla kez güvenle çalıştırılabilir)

#### Ön Gereksinimler

1. Çalışan bir Dokploy instance'ı
2. Dokploy ile yapılandırılmış bir domain adı (SSL otomatik olarak Let's Encrypt ile sağlanır)

#### Deployment Adımları

1. **Dokploy dashboard'unuzda yeni bir Docker Compose uygulaması oluşturun**

2. **Repository'nizi bağlayın:**
   - GitHub/GitLab/Bitbucket'tan bu repository'yi seçin
   - Veya Git URL'sini doğrudan kullanın
   - Branch: `master`

3. **Dokploy'un Environment sekmesinde environment variable'ları yapılandırın:**

   Tüm yapılandırma environment variable'lar ile yapılır - manuel dosya düzenleme gerekmez!

   **Gerekli Variable'lar:**
   ```env
   # Django Core
   SECRET_KEY=your-secret-key-here-min-50-chars
   DJANGO_ALLOWED_HOSTS=.yourdomain.com yourdomain.com localhost 127.0.0.1
   CSRF_TRUSTED_ORIGINS=https://yourdomain.com

   # Uygulama Ayarları
   APP_DOMAIN=yourdomain.com
   APP_PROTOCOL=https
   APP_FROM_EMAIL=noreply@yourdomain.com

   # Veritabanı
   POSTGRES_USER=db_dictionary_user
   POSTGRES_PASSWORD=guclu-sifre-buraya
   POSTGRES_DB=db_dictionary
   SQL_USER=db_dictionary_user
   SQL_PASSWORD=guclu-sifre-buraya
   SQL_DATABASE=db_dictionary
   ```

   > ⚠️ **ÖNEMLİ**: `DJANGO_ALLOWED_HOSTS` **boşlukla ayrılmış** olmalıdır, virgülle değil!
   > Örnek: `.yourdomain.com yourdomain.com localhost`

   **İsteğe Bağlı Variable'lar:**
   ```env
   # E-posta (e-posta fonksiyonunu devre dışı bırakmak için boş bırakın)
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-specific-password

   # Otomatik Superuser Oluşturma
   DJANGO_SUPERUSER_USERNAME=admin
   DJANGO_SUPERUSER_EMAIL=admin@yourdomain.com
   DJANGO_SUPERUSER_PASSWORD=guclu-admin-sifresi

   # Redis & RabbitMQ (varsayılanlar çoğu durum için yeterlidir)
   REDIS_URL=redis://redis:6379/
   RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/

   # Debug modu (0=kapalı, 1=açık - production için 0 tutun)
   DEBUG=0
   ```

   **Tüm Environment Variable'lar:**

   | Variable | Gerekli | Varsayılan | Açıklama |
   |----------|---------|------------|----------|
   | `SECRET_KEY` | ✅ Evet | - | Django gizli anahtarı (min 50 karakter) |
   | `DJANGO_ALLOWED_HOSTS` | ✅ Evet | - | Django'nun hizmet vereceği boşlukla ayrılmış domain'ler |
   | `CSRF_TRUSTED_ORIGINS` | ✅ Evet | - | CSRF için güvenilen origin'ler (https:// ile) |
   | `APP_DOMAIN` | ✅ Evet | - | Birincil domain (e-postalar/URL'lerde kullanılır) |
   | `APP_PROTOCOL` | ❌ Hayır | `https` | Protokol (http veya https) |
   | `APP_FROM_EMAIL` | ✅ Evet | - | Giden e-postalar için From adresi |
   | `POSTGRES_USER` | ✅ Evet | - | PostgreSQL kullanıcı adı |
   | `POSTGRES_PASSWORD` | ✅ Evet | - | PostgreSQL şifresi |
   | `POSTGRES_DB` | ✅ Evet | - | PostgreSQL veritabanı adı |
   | `SQL_USER` | ✅ Evet | - | Django veritabanı kullanıcısı (POSTGRES_USER ile eşleşmeli) |
   | `SQL_PASSWORD` | ✅ Evet | - | Django veritabanı şifresi (POSTGRES_PASSWORD ile eşleşmeli) |
   | `SQL_DATABASE` | ✅ Evet | - | Django veritabanı adı (POSTGRES_DB ile eşleşmeli) |
   | `EMAIL_HOST` | ❌ Hayır | - | SMTP sunucu hostname'i |
   | `EMAIL_PORT` | ❌ Hayır | `587` | SMTP sunucu portu |
   | `EMAIL_HOST_USER` | ❌ Hayır | - | SMTP kullanıcı adı |
   | `EMAIL_HOST_PASSWORD` | ❌ Hayır | - | SMTP şifresi |
   | `DJANGO_SUPERUSER_USERNAME` | ❌ Hayır | - | Otomatik admin kullanıcı adı |
   | `DJANGO_SUPERUSER_EMAIL` | ❌ Hayır | - | Otomatik admin e-postası |
   | `DJANGO_SUPERUSER_PASSWORD` | ❌ Hayır | - | Otomatik admin şifresi |
   | `REDIS_URL` | ❌ Hayır | `redis://redis:6379/` | Redis bağlantı URL'si |
   | `RABBITMQ_URL` | ❌ Hayır | `amqp://guest:guest@rabbitmq:5672/` | RabbitMQ bağlantı URL'si |
   | `DEBUG` | ❌ Hayır | `0` | Debug modu (0=kapalı, 1=açık) |

   **SECRET_KEY Nasıl Oluşturulur:**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

   Tüm variable'ların detaylı açıklamaları için `.env.example` dosyasına bakın.

4. **Deploy:**
   - Dokploy'da "Deploy" butonuna tıklayın
   - Entrypoint scripti otomatik olarak:
     - PostgreSQL'in hazır olmasını bekler
     - Veritabanı migration'larını çalıştırır (`python manage.py migrate`)
     - Statik dosyaları toplar (`python manage.py collectstatic`)
     - Quicksetup ile varsayılan kullanıcıları oluşturur (`python manage.py quicksetup`)
     - ENV variable'lar ayarlanmışsa superuser oluşturur (`python manage.py createsuperuser`)
     - Volume izinlerini düzeltir
     - Uygulamayı Gunicorn ile başlatır
   - Tüm servisler health check'ler ve uygun bağımlılıklarla başlar
   - **Manuel komut gerekmez!**

5. **Domain'inizi yapılandırın:**
   - Dokploy'un Domains ayarlarına domain'inizi ekleyin
   - SSL sertifikaları Let's Encrypt ile otomatik olarak sağlanır
   - Traefik (Dokploy'un reverse proxy'si) tüm HTTPS/SSL termination'ını yönetir

6. **Sitenize erişin:**
   - Domain'inize gidin
   - Superuser kimlik bilgilerinizle giriş yapın (otomatik oluşturulduysa)
   - Her şey kullanıma hazır!

#### Özellikler

✅ **Sıfır manuel CLI komutu** - Her şey deployment'ta otomatik çalışır
✅ **Otomatik SSL/TLS** - Dokploy, Let's Encrypt ile sertifikaları yönetir
✅ **Kalıcı depolama** - Tüm veriler (veritabanı, medya, statik) Dokploy volume'lerinde saklanır
✅ **Otomatik iyileşme** - Container'lar hata durumunda otomatik yeniden başlar
✅ **Kolay güncellemeler** - Repository'nize push yapın veya yeniden deploy'a tıklayın
✅ **Otomatik superuser oluşturma** - Tek tıkla admin hesabı için ENV variable'ları ayarlayın
✅ **İdempotent deployment'lar** - Birden fazla kez güvenle yeniden deploy edilebilir
✅ **Entegre loglama** - Tüm log'lara Dokploy UI üzerinden erişilebilir

#### Servis Mimarisi

Deployment 7 containerize edilmiş servisi içerir:

- **db** (PostgreSQL 17.6) - Health check'li ana veritabanı
- **redis** (Redis 8.2) - Önbellekleme katmanı ve oturum depolama
- **rabbitmq** (RabbitMQ 4.1) - Celery görevleri için mesaj broker'ı
- **web** (Django 5.2 + Gunicorn) - 4 worker ile ana uygulama
- **celery-worker** - Arka plan görevlerini asenkron işler
- **celery-beat** - Planlanmış periyodik görevleri yönetir
- **nginx** - Reverse proxy ve statik dosya sunucusu

Tüm servisler `dokploy-network` üzerinden iletişim kurar ve uygun health check'lere ve başlatma bağımlılıklarına sahiptir.

#### Sorun Giderme

**400 Bad Request Hatası:**
- `DJANGO_ALLOWED_HOSTS`'un **boşlukla ayrılmış** olduğundan emin olun, virgülle değil
- Örnek: `DJANGO_ALLOWED_HOSTS=.yourdomain.com yourdomain.com localhost`
- Hem wildcard subdomain'i (`.yourdomain.com`) hem de root domain'i dahil edin

**Container'lar Dokploy Terminal'de Görünmüyor:**
- Özel `container_name` direktiflerinin ayarlanmadığından emin olun (docker-compose.yml'de zaten düzeltildi)
- Tüm servislerin `dokploy-network` üzerinde olduğunu doğrulayın

**Volume'lerde İzin Hataları:**
- Entrypoint scripti `/app/static` ve `/app/media` üzerindeki izinleri otomatik düzeltir
- Container'lar önce root olarak çalışır, izinleri düzeltir, sonra `django` kullanıcısına geçer

**Veritabanı Bağlantı Sorunları:**
- Veritabanı kimlik bilgilerinin tüm servislerde eşleştiğini kontrol edin (web, celery-worker, celery-beat)
- `SQL_HOST=db` olduğundan emin olun (servis adı, container adı değil)
- Web başlamadan önce PostgreSQL health check'inin geçtiğini doğrulayın

**Statik Dosyalar Yüklenmiyor:**
- Nginx, statik dosyaları `/app/static` volume'ünden sunar
- Entrypoint, deployment'ta otomatik olarak `collectstatic --noinput` çalıştırır
- Nginx log'larını kontrol edin: `dokploy logs -f <app-name> --service nginx`

**RabbitMQ Bağlantı Sorunları:**
- `RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/` olduğundan emin olun
- RabbitMQ'nun ilk başlatmada sağlıklı hale gelmesi ~10-15 saniye sürer
- Dokploy dashboard'unda health durumunu kontrol edin

**Log'ları Görüntüleme:**
`dokploy` CLI veya Dokploy UI kullanın:
```bash
dokploy logs -f <app-name> --service web
dokploy logs -f <app-name> --service db
dokploy logs -f <app-name> --service nginx
```

#### Notlar

- Proje kök dizinindeki `docker-compose.yml` özellikle Dokploy için yapılandırılmıştır
- Geleneksel deployment için ilk bölümde açıklanan Makefile yöntemini kullanın
- Tüm servisler Docker dahili ağı üzerinden iletişim kurar (servis adları hostname olarak)
- Volume'ler docker-compose.yml'e göre `../files/` içinde saklanır (Dokploy standardı)
- Nginx yalnızca HTTP'yi yönetir (port 80) - Traefik (Dokploy'un reverse proxy'si) HTTPS/SSL'i yönetir
- Superuser oluşturma isteğe bağlıdır ancak ilk kurulum için önerilir
- Deployment, yeniden üretilebilirlik için sabitlenmiş Docker image SHA256 hash'lerini kullanır
