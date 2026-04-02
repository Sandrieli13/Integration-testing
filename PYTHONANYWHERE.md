# Deploying this project on PythonAnywhere

## 1. Clone and virtualenv

```bash
cd ~
git clone -b LucasYao_this_branch_for_myself https://github.com/Sandrieli13/Integration-testing.git
cd Integration-testing
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
```

### Disk quota (free account)

The default `requirements.txt` is **minimal** (no NumPy/Pandas/Matplotlib) so installs fit small quotas. If you still see **Disk quota exceeded**:

- `rm -rf ~/.cache/pip`
- `du -h ~ | sort -h | tail -15` — delete unused large folders (old clones, duplicate venvs)
- Re-run: `pip install --no-cache-dir -r requirements.txt`

Optional local analytics stack: `requirements-dev.txt` (do not install on PA unless you upgrade disk).

If `pip` errors with `\x00` in `requirements.txt`, the file was saved as UTF-16. Fix on the server with:

`python3 -c "p='requirements.txt'; open(p,'wb').write(open(p,'r',encoding='utf-16').read().encode('utf-8'))"`

(or `git pull` after the repo is fixed to UTF-8).

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

## 4. Static files (CSS / layout)

The project uses **WhiteNoise** so Django can serve `/static/` when `DEBUG` is false. You still must run **`collectstatic`** after every deploy.

```bash
cd ~/Integration-testing
source venv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --noinput
```

Check that files exist, e.g.:

```bash
ls ~/Integration-testing/static/webflow.css
```

**Option A — rely on WhiteNoise (simplest):**  
On the **Web** tab, under **Static files**, **remove** any `/static/` mapping (or leave it unset). Reload the site. Requests to `/static/...` then go through Django + WhiteNoise.

**Option B — PythonAnywhere nginx (faster):**  
Add mapping: URL `/static/` → directory `/home/YOURUSERNAME/Integration-testing/static`  
If the path is wrong, the site loads but **CSS disappears** (404 on `.css` files). Fix the directory or use Option A.

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

### “Something went wrong” / blank error (site won’t load)

The app process is crashing. **Open the Web tab → Error log** and scroll to the **bottom**; the last traceback is what matters.

**In a Bash console**, run (use your username; copy env lines from your WSGI file if you like):

```bash
cd ~/Integration-testing
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=mysite.settings
export DJANGO_DEBUG=false
export DJANGO_ALLOWED_HOSTS=YOURUSERNAME.pythonanywhere.com
export DJANGO_CSRF_TRUSTED_ORIGINS=https://YOURUSERNAME.pythonanywhere.com
export DJANGO_SECRET_KEY=test-key-not-for-production
python -c "import django; django.setup(); from django.core.wsgi import get_wsgi_application; get_wsgi_application(); print('WSGI OK')"
```

- **`ModuleNotFoundError`** (e.g. `whitenoise`, `django`): Web tab **Virtualenv** must point at this project’s `venv`, then `pip install --no-cache-dir -r requirements.txt`.
- Wrong **project path** in WSGI: `project_home` must be the folder containing **`manage.py`** (e.g. `Integration-testing`), not `mysite` inside it.

**Temporary debug:** in the WSGI file only, set `os.environ["DJANGO_DEBUG"] = "true"` and reload. Django will show a **yellow error page** with the real exception (turn it back to `false` after fixing).

**Disable WhiteNoise** (if you use the Web tab `/static/` → `.../Integration-testing/static` mapping): in WSGI, before `get_wsgi_application()`:

`os.environ["DJANGO_USE_WHITENOISE"] = "false"`
