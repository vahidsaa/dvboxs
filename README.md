عالی. `requirements.txt` آماده است. اما برای سروری که اینترنت ندارد، باید **نحوه نصب دستی** را در `README.md` توضیح دهیم.

## ✅ مرحله دوم: ساخت `README.md` کامل

دستور زیر را بزنید تا فایل ایجاد شود:

```bash
cat > /home/dvboxs/README.md << 'EOF'
# پروژه ویباکس (Vboxs.ir) - فروشگاه آنلاین کارتن‌سازی صالحی

## توضیحات پروژه
فروشگاه آنلاین خرید کارتن، جعبه پستی، کارتن اسباب‌کشی، جعبه دایکاتی و لمینتی.  
توسعه یافته با **Django 5.2** و استفاده از **SQLite** به عنوان دیتابیس.

---

## نحوه دیپلوی روی سرور ایران (بدون دسترسی مستقیم به اینترنت)

### پیش‌نیازها
- سرور با سیستم‌عامل Ubuntu 22.04 یا بالاتر
- دسترسی روت (root) به سرور
- دامنه فعال (vboxs.ir) با تنظیمات DNS در ArvanCloud

---

### مرحله 1: اتصال به سرور
```bash
ssh root@87.248.145.148 -p 9011
```

### مرحله 2: به‌روزرسانی سیستم و نصب پیش‌نیازها
```bash
apt update && apt upgrade -y
apt install -y python3-pip python3-dev nginx uwsgi uwsgi-plugin-python3 build-essential gcc git
```

### مرحله 3: ایجاد محیط مجازی
```bash
mkdir -p /home/env
cd /home/env
python3 -m venv vboxs
source /home/env/vboxs/bin/activate
```

### مرحله 4: دریافت پروژه از گیت‌هاب
```bash
cd /home
git clone https://github.com/vahidsaa/dvboxs.git
```

### مرحله 5: نصب پکیج‌های پایتون (به صورت دستی - به دلیل محدودیت اینترنت ایران)

**روش کار:** روی یک ماشین دیگر با اینترنت آزاد، فایل‌های wheel مورد نیاز را دانلود کرده، سپس با SCP به سرور منتقل کنید.

**لیست پکیج‌ها و نسخه‌ها:**
```
asgiref==3.11.1
Django==5.2.14
django-phonenumber-field==8.4.0
phonenumbers==9.0.31
pillow==12.2.0
psycopg2-binary==2.9.12
setuptools==82.0.1
sqlparse==0.5.5
tzdata==2026.2
uWSGI==2.0.31
```

**نصب روی سرور:**
```bash
pip install /home/env/django_packages/asgiref-3.11.1-py3-none-any.whl
pip install /home/env/django_packages/Django-5.2.14-py3-none-any.whl
pip install /home/env/django_packages/django_phonenumber_field-8.4.0-py3-none-any.whl
pip install /home/env/django_packages/phonenumbers-9.0.31-py2.py3-none-any.whl
pip install /home/env/django_packages/pillow-12.2.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl
pip install /home/env/django_packages/psycopg2_binary-2.9.12-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl
pip install /home/env/django_packages/setuptools-82.0.1-py3-none-any.whl
pip install /home/env/django_packages/sqlparse-0.5.5-py3-none-any.whl
pip install /home/env/django_packages/tzdata-2026.2-py2.py3-none-any.whl
```

**نصب uWSGI از سورس:**
```bash
cd /home/env/django_packages
tar -xzf uwsgi-2.0.31.tar.gz
cd uwsgi-2.0.31
python setup.py install
```

### مرحله 6: تنظیمات Django
```bash
cd /home/dvboxs
nano vboxs/settings.py
```

تغییرات الزامی:
```python
DEBUG = False
ALLOWED_HOSTS = ['87.248.145.148', 'vboxs.ir', 'localhost']
STATIC_ROOT = '/home/dvboxs/staticfiles'
```

سپس:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### مرحله 7: تنظیمات uWSGI

فایل `/home/dvboxs/uwsgi.ini`:
```ini
[uwsgi]
chdir = /home/dvboxs
module = vboxs.wsgi:application
home = /home/env/vboxs
master = true
processes = 2
socket = /home/dvboxs/uwsgi.sock
chmod-socket = 666
vacuum = true
enable-threads = true
die-on-term = true
logto = /home/dvboxs/uwsgi.log
```

### مرحله 8: سرویس systemd

فایل `/etc/systemd/system/dvboxs.service`:
```ini
[Unit]
Description=uWSGI service for dvboxs project
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/dvboxs
ExecStart=/home/env/vboxs/bin/uwsgi --ini /home/dvboxs/uwsgi.ini
Restart=always
RestartSec=5
KillSignal=SIGINT
TimeoutStopSec=5

[Install]
WantedBy=multi-user.target
```

فعال‌سازی سرویس:
```bash
systemctl daemon-reload
systemctl enable dvboxs.service
systemctl start dvboxs.service
```

### مرحله 9: تنظیمات Nginx

فایل `/etc/nginx/sites-available/dvboxs.conf`:
```nginx
server {
    listen 80;
    listen 443 ssl;
    server_name 87.248.145.148 vboxs.ir;
    charset utf-8;
    client_max_body_size 75M;

    ssl_certificate /etc/nginx/ssl/vboxs.ir.crt;
    ssl_certificate_key /etc/nginx/ssl/vboxs.ir.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location /static {
        alias /home/dvboxs/staticfiles;
    }

    location /media {
        alias /home/dvboxs/media;
    }

    location / {
        include uwsgi_params;
        uwsgi_pass unix:///home/dvboxs/uwsgi.sock;
    }
}
```

فعال‌سازی سایت:
```bash
ln -s /etc/nginx/sites-available/dvboxs.conf /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
```

---

## مرحله 10: SSL (گواهی امنیت)

به دلیل محدودیت اینترنت ایران، گواهی SSL به صورت دستی و با DNS challenge دریافت می‌شود.

**روی یک لپ‌تاپ لینوکس با اینترنت آزاد:**
```bash
sudo apt install certbot -y
sudo certbot certonly --manual --preferred-challenges dns -d vboxs.ir -d www.vboxs.ir
```

سپس رکوردهای TXT را در **ArvanCloud** اضافه کرده و پس از انتشار، Enter بزنید.

**کپی گواهی به سرور ایران:**
```bash
scp -P 9011 /etc/letsencrypt/live/vboxs.ir/fullchain.pem root@87.248.145.148:/etc/nginx/ssl/vboxs.ir.crt
scp -P 9011 /etc/letsencrypt/live/vboxs.ir/privkey.pem root@87.248.145.148:/etc/nginx/ssl/vboxs.ir.key
```

**تنظیمات ArvanCloud:**
- Origin Connection: HTTP
- Activate HTTPS: Enabled
- Minimum TLS Version: 1.2

---

## عیب‌یابی سریع

| مشکل | راه‌حل |
|------|-------|
| 502 Bad Gateway | `systemctl restart dvboxs.service && systemctl restart nginx` |
| فایل‌های استاتیک نمایش داده نمی‌شوند | `python manage.py collectstatic --noinput` سپس `systemctl restart nginx` |
| خطای SSL | در ArvanCloud، Origin Connection را روی HTTP قرار دهید |
| خطای 404 صفحه | بررسی کنید `ALLOWED_HOSTS` در settings.py درست باشد |

---

## نگهداری و تمدید SSL (هر 85 روز یکبار)

مراحل دریافت گواهی جدید (روی لپ‌تاپ لینوکس با اینترنت آزاد):
```bash
sudo certbot certonly --manual --preferred-challenges dns -d vboxs.ir -d www.vboxs.ir
```
سپس رکوردهای TXT جدید را در ArvanCloud به‌روزرسانی کرده و کپی فایل‌ها به سرور.

---

## تماس و پشتیبانی

- ایمیل: vboxs.help@gmail.com
- تلفن: ۰۲۱-۵۵۰۶۰۲۸۸
- آدرس: تهران، خیابان رجایی، سه راه ابریشم، خیابان همدانی، نهر فیروزآبادی، روبروی پارک بهاران

---

**تاریخ آخرین به‌روزرسانی:** ۴ ژوئن ۲۰۲۶
EOF
```

---

## ✅ مرحله سوم: تأیید و ارسال به گیت‌هاب

فایل README ساخته شد. حالا فایل‌ها را به گیت اضافه می‌کنیم:

```bash
cd /home/dvboxs
git add requirements.txt README.md
git commit -m "Add requirements.txt and comprehensive README for deployment on Iran server"
git push origin main
```

خروجی دستور `git push` را بفرستید تا ببینیم موفق بوده یا نه.

**بعد از آن، کارهای گوگل (Search Console) تمام شده و پروژه روی گیت‌هاب به‌روزرسانی شده است.**
