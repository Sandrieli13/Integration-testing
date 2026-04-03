# =============================================================================
# PythonAnywhere → Web tab → WSGI configuration file
#
# Copy this entire file into the editor PythonAnywhere shows for your site, OR
# save as this path on PA and point "WSGI configuration file" at it if you use a custom path.
#
# Replace every YOUR_* placeholder before Reload. Do not commit real secrets to GitHub.
# =============================================================================

import os
import sys

# Project root (same folder as manage.py)
project_home = "/home/YOURUSERNAME/Integration-testing"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# --- Django ---
os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"
os.environ["DJANGO_DEBUG"] = "false"
os.environ["DJANGO_ALLOWED_HOSTS"] = "YOURUSERNAME.pythonanywhere.com"
os.environ["DJANGO_CSRF_TRUSTED_ORIGINS"] = "https://YOURUSERNAME.pythonanywhere.com"
os.environ["DJANGO_SECRET_KEY"] = "YOUR_LONG_RANDOM_SECRET_KEY_HERE"

# --- BLS live tech career stats (OEWS) — optional but recommended ---
os.environ["BLS_API_KEY"] = "YOUR_BLS_REGISTRATION_KEY_HERE"
# Optional: 7-digit metro CBSA for OEWS (leave unset for U.S. national)
# os.environ["BLS_OEWS_METRO_AREA_CODE"] = "0356200"

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
