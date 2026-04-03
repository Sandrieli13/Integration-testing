# Integration-testing (BMCC Connect)

Django project for **BMCC student tools**: course planning, clubs, mentors, career readiness (Careers + Experiential Learning hub), campus data analysis, and pathway electives.

**Active development branch:** `BMCConnect_Public`

Upstream repo: [Sandrieli13/Integration-testing](https://github.com/Sandrieli13/Integration-testing).
BMCCONNECT Website: https://lucasyao111.pythonanywhere.com/
## Stack

- **Python 3.9+** (match your host; PythonAnywhere web app uses 3.9 in this setup)
- **Django 4.2**
- **SQLite** (default; `db.sqlite3` is gitignored)
- **WhiteNoise** for static files in production (optional; see `DJANGO_USE_WHITENOISE`)

## Local setup

```bash
git clone -b LucasYao_this_branch_for_myself https://github.com/Sandrieli13/Integration-testing.git
cd Integration-testing
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Optional heavier packages for local scraping/plots (numpy, pandas, matplotlib, seaborn):

```bash
pip install -r requirements-dev.txt
```

Run migrations and dev server:

```bash
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Loading data

`migrate` creates **empty** tables. Use management commands or your own `db.sqlite3`.

| Command | Purpose |
|--------|---------|
| `python manage.py load_json_data` | Majors, courses, semesters from `base/fixtures/sql_code.json` |
| `python manage.py load_elective_courses` | Pathway/program electives from `base/fixtures/elective_courses.json` (no network; good for PythonAnywhere) |
| `python manage.py dump_elective_courses` | **Export** electives fixture after refreshing data locally |
| `python manage.py sync_department_metrics` | `DepartmentMetric` rows for Data Analysis charts (CSVs under `client/css/csv/`) |
| `python manage.py import_individual_society_bmcc` (etc.) | Live BMCC scrape; needs network; often blocked on free PythonAnywhere |

**Careers** app data (majors/jobs/skills) is not in the JSON fixtures; load via uploaded `db.sqlite3`, admin, or custom import.

## Deployment (PythonAnywhere)

See **[PYTHONANYWHERE.md](./PYTHONANYWHERE.md)** for WSGI, virtualenv, static files, environment variables, and troubleshooting.

## Project layout (short)

| Path | Notes |
|------|--------|
| `mysite/` | Settings, root URLs |
| `myapp/` | Auth, home, mentors, profiles |
| `base/` | Courses, electives, Data Analysis, BMCC metrics |
| `apps/clubs/` | Clubs UI and club chart |
| `careers/` | Majors, jobs, skills, internship matcher |
| `experientiallearning/` | Career readiness EL hub (templates + static) |
| `client/html/` | Shared templates and partials |
| `client/css/`, `client/js/`, `client/images/` | Collected as static assets |

## Contributing / encoding

- Save `requirements.txt` as **UTF-8** (not UTF-16) so `pip` can parse it.
- Line endings: see `.gitattributes`.

## License

Not specified in this branch; use the license chosen by the upstream repository owners.
