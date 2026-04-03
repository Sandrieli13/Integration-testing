"""
Refresh cached BLS OEWS data for the Tech career statistics page.

Requires BLS_API_KEY (see mysite/settings.py). Run after deploy or when you want
new OEWS figures without waiting for the cache TTL.

  python manage.py refresh_tech_career_bls
"""

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from careers.bls_oews_client import bls_api_smoke_test, load_or_fetch_tech_oews


class Command(BaseCommand):
    help = "Fetch BLS OEWS series for tech career charts and update the on-disk cache."

    def handle(self, *args, **options):
        key = getattr(settings, "BLS_API_KEY", "") or ""
        if not key:
            self.stderr.write(
                self.style.ERROR(
                    "BLS_API_KEY is not set. Register at https://data.bls.gov/registrationEngine/ "
                    "and set the environment variable (e.g. in WSGI config on PythonAnywhere)."
                )
            )
            raise SystemExit(1)

        base = Path(settings.BASE_DIR)
        metro = getattr(settings, "BLS_OEWS_METRO_AREA_CODE", "") or ""
        metro_code = metro if len(metro) == 7 and metro.isdigit() else None
        cache_hours = int(getattr(settings, "BLS_TECH_MARKET_CACHE_HOURS", 24))
        prefer_year = getattr(settings, "BLS_OEWS_PREFER_YEAR", None)

        result = load_or_fetch_tech_oews(
            key,
            base,
            cache_hours=cache_hours,
            metro_area_code=metro_code,
            prefer_year=prefer_year,
            force_refresh=True,
        )
        if result is None:
            self.stderr.write(
                self.style.ERROR(
                    "BLS request failed or returned incomplete series. Check API key, network, and BLS status."
                )
            )
            self.stderr.write(self.style.WARNING("--- BLS smoke test (one series) ---"))
            self.stderr.write(bls_api_smoke_test(key))
            raise SystemExit(1)

        _openings, _salary, year, geo = result
        self.stdout.write(self.style.SUCCESS(f"Cached OEWS {year} · {geo}"))
