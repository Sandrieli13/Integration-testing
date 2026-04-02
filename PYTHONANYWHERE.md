# Deploying this project on PythonAnywhere

## 1. Clone and virtualenv

```bash
cd ~
git clone https://github.com/Sandrieli13/Integration-testing.git
cd Integration-testing
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Use the same Python version you selected for the web app (3.9–3.11 is fine).

## 2. Web tab → Virtualenv

Set to: `/home/YOURUSERNAME/Integration-testing/venv` (adjust path).

## 3. WSGI configuration file

Replace the file contents with (edit paths and secrets):

```python
import os
import sys

project_home = "/home/YOURUSERNAME/Integration-testing"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"
os.environ["DJANGO_DEBUG"] = "false"
os.environ["DJANGO_ALLOWED_HOSTS"] = "YOURUSERNAME.pythonanywhere.com"
os.environ["DJANGO_CSRF_TRUSTED_ORIGINS"] = "https://YOURUSERNAME.pythonanywhere.com"
os.environ["DJANGO_SECRET_KEY"] = "generate-a-long-random-string-here"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 4. Static files

```bash
cd ~/Integration-testing
source venv/bin/activate
python manage.py collectstatic --noinput
```

**Web** tab → **Static files**: URL `/static/` → directory  
`/home/YOURUSERNAME/Integration-testing/static`

## 5. Database

```bash
python manage.py migrate
python manage.py createsuperuser   # optional
```

`db.sqlite3` is not in git; the server creates a fresh DB on first migrate.

## 6. Reload

Use the green **Reload** button on the Web tab.

## Troubleshooting

- Read **Error log** and **Server log** on the Web tab.
- `DisallowedHost`: fix `DJANGO_ALLOWED_HOSTS`.
- CSRF errors on login/forms: ensure `DJANGO_CSRF_TRUSTED_ORIGINS` uses `https://` and matches your site URL exactly.
