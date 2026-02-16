# LuxeHome - Online Furniture Shop

A full-featured online furniture e-commerce website built with Django. Includes product catalog with filtering, image slideshows, favorites, shopping cart, pay-on-delivery checkout, Telegram order notifications, and user accounts.

---

## Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Local Development Setup](#local-development-setup)
5. [Admin Panel](#admin-panel)
6. [Telegram Notifications Setup](#telegram-notifications-setup)
7. [Deployment to Production Server](#deployment-to-production-server)
   - [Option A: Deploy on Ubuntu/Linux VPS](#option-a-deploy-on-ubuntulinux-vps)
   - [Option B: Deploy on Railway/Render (PaaS)](#option-b-deploy-on-railwayrender-paas)
8. [Environment Variables](#environment-variables)
9. [Managing Products & Content](#managing-products--content)
10. [Troubleshooting](#troubleshooting)

---

## Features

- **Homepage** with banner image slideshow (Swiper.js)
- **Product catalog** with filters (category, price, material, color) and search
- **Product cards** with image slideshow, discount badges, favorites button, add-to-cart button
- **Product detail page** with image gallery/thumbnails, specifications, related products
- **Shopping cart** (session-based, works for guests and logged-in users)
- **Checkout** with pay-on-delivery (no online payment required)
- **Telegram notifications** sent to shop owner on every new order
- **User accounts** (signup, login, profile editing, avatar upload)
- **Favorites/Wishlist** with AJAX toggle
- **Order history** for logged-in users
- **Responsive design** (mobile-friendly, Bootstrap 5)
- **Django Admin** for full content management

---

## Tech Stack

| Component     | Technology                        |
|---------------|-----------------------------------|
| Backend       | Python 3.12, Django 5+            |
| Database      | SQLite (development), PostgreSQL (production) |
| Frontend      | Django Templates, Bootstrap 5     |
| Slideshows    | Swiper.js                         |
| Image Upload  | Pillow                            |
| Filtering     | django-filter                     |
| Notifications | Telegram Bot API (via requests)   |

---

## Project Structure

```
lession/
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── db.sqlite3                 # SQLite database (auto-created)
│
├── furniture_shop/            # Project settings
│   ├── settings.py            # Main configuration
│   ├── urls.py                # Root URL routing
│   └── wsgi.py                # WSGI entry point
│
├── core/                      # Homepage, banners, static pages
│   ├── models.py              # Banner model
│   ├── views.py               # Home, About, Contact views
│   ├── urls.py
│   └── templates/core/
│       ├── home.html
│       ├── about.html
│       └── contact.html
│
├── products/                  # Catalog and product detail
│   ├── models.py              # Category, Product, ProductImage
│   ├── views.py               # Catalog list, product detail
│   ├── filters.py             # django-filter configuration
│   ├── urls.py
│   └── templates/products/
│       ├── _product_card.html # Reusable product card component
│       ├── catalog.html
│       └── product_detail.html
│
├── accounts/                  # User authentication and profiles
│   ├── models.py              # UserProfile
│   ├── forms.py               # Signup, profile edit forms
│   ├── views.py               # Signup, login, logout, profile
│   ├── urls.py
│   └── templates/accounts/
│       ├── signup.html
│       ├── login.html
│       └── profile.html
│
├── cart/                      # Cart, checkout, orders
│   ├── models.py              # Order, OrderItem
│   ├── views.py               # Cart, checkout, order history
│   ├── context_processors.py  # Cart count in navbar
│   ├── telegram.py            # Telegram notification sender
│   ├── urls.py
│   └── templates/cart/
│       ├── cart.html
│       ├── checkout.html
│       ├── order_success.html
│       └── order_history.html
│
├── favorites/                 # Wishlist/favorites
│   ├── models.py              # Favorite model
│   ├── views.py               # Toggle favorite, list favorites
│   ├── urls.py
│   └── templates/favorites/
│       └── favorites.html
│
├── templates/                 # Shared templates
│   └── base.html              # Base layout (navbar, footer)
│
├── static/                    # Static assets
│   ├── css/style.css          # Custom styles
│   ├── js/main.js             # Cart/favorites AJAX, toasts
│   └── img/                   # Static images
│
└── media/                     # User-uploaded files (images)
    ├── banners/               # Banner images
    ├── products/              # Product images
    ├── categories/            # Category images
    └── avatars/               # User avatars
```

---

## Local Development Setup

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Step-by-step

```bash
# 1. Clone or copy the project
cd lession

# 2. (Optional) Create a virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run database migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create a superuser for admin access
python manage.py createsuperuser

# 6. (Optional) Load sample data
python seed_data.py

# 7. (Optional) Download product images
python download_real_images.py

# 8. Start the development server
python manage.py runserver
```

Open your browser: **http://127.0.0.1:8000/**

---

## Admin Panel

**URL:** http://127.0.0.1:8000/admin/

Default credentials (from seed script):
- Username: `admin`
- Password: `admin123`

### What you can manage:

| Section    | What you can do                                              |
|------------|--------------------------------------------------------------|
| Banners    | Add/edit homepage slideshow banners (image, title, subtitle, link, order) |
| Categories | Create categories and subcategories with images              |
| Products   | Add products with multiple images (inline upload), set prices, discounts, material, color, stock |
| Orders     | View all orders, change order status (pending → confirmed → shipped → delivered) |
| Users      | Manage user accounts and profiles                            |
| Favorites  | View user wishlists                                          |

### Adding a new product (step by step):

1. Go to Admin → Products → Add Product
2. Fill in: name, slug, category, description, price
3. Optionally set: old_price (for discount), material, color, dimensions, weight
4. Set stock quantity and check "Is featured" to show on homepage
5. Scroll down to **Product Images** section → upload multiple images
6. Check "Is primary" on the main image
7. Click Save

---

## Telegram Notifications Setup

When a customer places an order, the shop owner receives a Telegram message with full order details.

### How to set up:

1. **Create a Telegram Bot:**
   - Open Telegram and search for `@BotFather`
   - Send `/newbot` and follow the instructions
   - Copy the **Bot Token** (looks like `123456789:ABCdefGHI...`)

2. **Get your Chat ID:**
   - Search for `@userinfobot` on Telegram
   - Send it any message
   - It will reply with your **Chat ID** (a number like `123456789`)

3. **Configure the project:**

   Set environment variables before running the server:

   **Windows (Command Prompt):**
   ```cmd
   set TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   set TELEGRAM_CHAT_ID=123456789
   python manage.py runserver
   ```

   **Windows (PowerShell):**
   ```powershell
   $env:TELEGRAM_BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
   $env:TELEGRAM_CHAT_ID="123456789"
   python manage.py runserver
   ```

   **Linux/Mac:**
   ```bash
   export TELEGRAM_BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
   export TELEGRAM_CHAT_ID="123456789"
   python manage.py runserver
   ```

4. **Test it:** Place a test order on the website. You should receive a message like:

   ```
   🛒 New Order #1
   ━━━━━━━━━━━━━━━
   👤 Customer: John Doe
   📞 Phone: +1234567890
   🏠 Address: 123 Main St, New York
   ━━━━━━━━━━━━━━━
   📦 Items:
     - Modern Velvet Sofa x1 = $1299.99
   ━━━━━━━━━━━━━━━
   💰 Total: $1299.99
   💳 Payment: Cash on Delivery
   ```

---

## Deployment to Production Server

### Option A: Deploy on Ubuntu/Linux VPS

This is the recommended method for a production deployment (DigitalOcean, AWS EC2, Linode, etc.).

#### 1. Server Preparation

```bash
# Connect to your server
ssh root@your-server-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib -y
```

#### 2. Create Database (PostgreSQL)

```bash
sudo -u postgres psql

CREATE DATABASE luxehome_db;
CREATE USER luxehome_user WITH PASSWORD 'your_strong_password_here';
ALTER ROLE luxehome_user SET client_encoding TO 'utf8';
ALTER ROLE luxehome_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE luxehome_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE luxehome_db TO luxehome_user;
\q
```

#### 3. Deploy Project Files

```bash
# Create project directory
sudo mkdir -p /var/www/luxehome
cd /var/www/luxehome

# Copy project files (from your local machine)
# Option 1: Using scp from your local machine:
#   scp -r e:\lession\* root@your-server-ip:/var/www/luxehome/
#
# Option 2: Using git (if you push to a repository):
#   git clone https://github.com/yourusername/luxehome.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

#### 4. Configure Production Settings

Create a `.env` file in the project root:

```bash
nano /var/www/luxehome/.env
```

Add these lines:

```env
DJANGO_SECRET_KEY=your-random-50-character-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-server-ip
DATABASE_URL=postgresql://luxehome_user:your_strong_password_here@localhost:5432/luxehome_db
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-telegram-chat-id
```

Update `furniture_shop/settings.py` for production — add at the top:

```python
import os

# Override for production
if os.environ.get('DJANGO_DEBUG') == 'False':
    DEBUG = False
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
    ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'luxehome_db',
            'USER': 'luxehome_user',
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

    STATIC_ROOT = BASE_DIR / 'staticfiles'
```

#### 5. Initialize Database & Static Files

```bash
cd /var/www/luxehome
source venv/bin/activate

# Load environment variables
export $(cat .env | xargs)

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# (Optional) Load sample data
python seed_data.py
```

#### 6. Configure Gunicorn (Application Server)

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/luxehome.service
```

Paste this content:

```ini
[Unit]
Description=LuxeHome Gunicorn Daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/luxehome
EnvironmentFile=/var/www/luxehome/.env
ExecStart=/var/www/luxehome/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/luxehome/luxehome.sock \
    furniture_shop.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl start luxehome
sudo systemctl enable luxehome
sudo systemctl status luxehome    # Verify it's running
```

#### 7. Configure Nginx (Web Server)

```bash
sudo nano /etc/nginx/sites-available/luxehome
```

Paste this content:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Max upload size (for product images)
    client_max_body_size 20M;

    # Static files
    location /static/ {
        alias /var/www/luxehome/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files (uploaded images)
    location /media/ {
        alias /var/www/luxehome/media/;
        expires 7d;
    }

    # Pass requests to Gunicorn
    location / {
        proxy_pass http://unix:/var/www/luxehome/luxehome.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/luxehome /etc/nginx/sites-enabled/
sudo nginx -t                  # Test configuration
sudo systemctl restart nginx
```

#### 8. Set File Permissions

```bash
sudo chown -R www-data:www-data /var/www/luxehome
sudo chmod -R 755 /var/www/luxehome/media
```

#### 9. SSL Certificate (HTTPS) — Free with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Certbot will automatically configure HTTPS and redirect HTTP to HTTPS.

#### 10. Verify Deployment

```bash
# Check all services are running
sudo systemctl status luxehome
sudo systemctl status nginx

# View logs if something is wrong
sudo journalctl -u luxehome -n 50
sudo tail -f /var/log/nginx/error.log
```

Visit: **https://yourdomain.com**

---

### Option B: Deploy on Railway/Render (PaaS)

For easier deployment without managing a server.

#### Railway

1. Push your code to GitHub
2. Go to [railway.app](https://railway.app) and create a new project
3. Connect your GitHub repository
4. Add a PostgreSQL database plugin
5. Set environment variables in Railway dashboard:
   - `DJANGO_SECRET_KEY` = (generate a random key)
   - `DJANGO_DEBUG` = `False`
   - `DJANGO_ALLOWED_HOSTS` = `your-app.railway.app`
   - `TELEGRAM_BOT_TOKEN` = your token
   - `TELEGRAM_CHAT_ID` = your chat ID
6. Add a `Procfile` in your project root:
   ```
   web: gunicorn furniture_shop.wsgi --bind 0.0.0.0:$PORT
   ```
7. Add `gunicorn` and `psycopg2-binary` to `requirements.txt`
8. Deploy

#### Render

1. Push your code to GitHub
2. Go to [render.com](https://render.com) and create a new Web Service
3. Connect your repository
4. Set:
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start Command: `gunicorn furniture_shop.wsgi`
5. Add environment variables in Render dashboard
6. Add a Render PostgreSQL database and connect it

---

## Environment Variables

| Variable              | Required | Description                                    | Example                            |
|-----------------------|----------|------------------------------------------------|------------------------------------|
| `DJANGO_SECRET_KEY`   | Production | Secret key for Django                         | `x8k2m...` (50+ random chars)     |
| `DJANGO_DEBUG`        | Production | Set to `False` for production                 | `False`                            |
| `DJANGO_ALLOWED_HOSTS`| Production | Comma-separated list of domains               | `yourdomain.com,www.yourdomain.com`|
| `TELEGRAM_BOT_TOKEN`  | Optional | Telegram bot token for order notifications     | `123456789:ABCdef...`              |
| `TELEGRAM_CHAT_ID`    | Optional | Telegram chat ID to receive notifications      | `123456789`                        |
| `DATABASE_URL`        | Production | PostgreSQL connection string                  | `postgresql://user:pass@host/db`   |

---

## Managing Products & Content

### Via Admin Panel (http://yourdomain.com/admin/)

**Add a Banner:**
1. Admin → Banners → Add Banner
2. Upload a wide image (recommended: 1920x600px)
3. Set title, subtitle, and optional link URL
4. Set order number (lower = shows first)
5. Check "Is active" to display it

**Add a Category:**
1. Admin → Categories → Add Category
2. Enter name and slug (e.g., "Living Room" / "living-room")
3. Upload a category image
4. Optionally select a parent category for subcategories

**Add a Product:**
1. Admin → Products → Add Product
2. Fill in all fields (name, slug, category, description, price, etc.)
3. In the "Product Images" section at the bottom, upload 3-5 photos
4. Mark one image as "Is primary" (this shows on the product card)
5. Set stock > 0 to make the product available for purchase

**Manage Orders:**
1. Admin → Orders → click an order
2. Change status: Pending → Confirmed → Shipped → Delivered
3. View all order items, customer info, and delivery address

---

## Troubleshooting

| Problem                          | Solution                                                        |
|----------------------------------|-----------------------------------------------------------------|
| Static files not loading         | Run `python manage.py collectstatic` and check STATIC_ROOT      |
| Media/images not showing         | Check MEDIA_URL and MEDIA_ROOT in settings.py; check Nginx config for /media/ |
| 500 Internal Server Error        | Check logs: `sudo journalctl -u luxehome -n 100`                |
| Telegram not sending             | Verify TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are set correctly |
| CSS/JS not updating              | Hard-refresh browser (Ctrl+Shift+R) or clear browser cache       |
| Database errors after changes    | Run `python manage.py makemigrations && python manage.py migrate` |
| Permission denied on media       | Run `sudo chown -R www-data:www-data /var/www/luxehome/media`    |
| Gunicorn not starting            | Check: `sudo journalctl -u luxehome -n 50` for error details    |
| Nginx 502 Bad Gateway            | Ensure Gunicorn is running: `sudo systemctl status luxehome`     |

### Useful Commands

```bash
# Restart application after code changes
sudo systemctl restart luxehome

# Restart Nginx after config changes
sudo systemctl restart nginx

# View live application logs
sudo journalctl -u luxehome -f

# Enter Django shell
cd /var/www/luxehome && source venv/bin/activate
python manage.py shell

# Create a new admin user
python manage.py createsuperuser

# Backup database
cp db.sqlite3 db.sqlite3.backup          # SQLite
pg_dump luxehome_db > backup.sql          # PostgreSQL
```

---

## License

This project is for educational purposes. Unsplash/Pexels images used under their free license terms.
