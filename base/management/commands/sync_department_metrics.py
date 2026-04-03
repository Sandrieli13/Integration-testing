from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from base.bmcc_pathway_scrape import fetch_page
from base.department_metrics import (
    CHART_DEFINITIONS,
    read_year_value_csv,
    read_year_value_csv_text,
    static_csv_abspath,
)
from base.models import DepartmentMetric


class Command(BaseCommand):
    help = (
        "Load DepartmentMetric rows from static CSV files (same source as the data analysis charts). "
        "Run after deploy or when CSV values change. "
        "With --fetch-from-web, download each CSV from BMCC_METRICS_CSV_BASE_URL + filename "
        "(mirror the files in client/css/csv/ on your own host or object storage)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--fetch-from-web",
            action="store_true",
            help=(
                "Download CSV bodies from settings.BMCC_METRICS_CSV_BASE_URL using each file's basename. "
                "Falls back to the local file if a download fails."
            ),
        )

    @transaction.atomic
    def handle(self, *args, **options):
        fetch_web = options["fetch_from_web"]
        base_url = getattr(settings, "BMCC_METRICS_CSV_BASE_URL", "") or ""

        if fetch_web and not base_url:
            self.stderr.write(
                self.style.WARNING(
                    "BMCC_METRICS_CSV_BASE_URL is empty; using local CSV files only. "
                    "Set the env var to your mirror base URL (no trailing slash)."
                )
            )
            fetch_web = False

        DepartmentMetric.objects.all().delete()
        bulk = []
        for spec in CHART_DEFINITIONS:
            path = static_csv_abspath(spec["csv"])
            fname = Path(spec["csv"]).name
            rows: list[list[int]] = []

            if fetch_web and base_url:
                url = f"{base_url}/{fname}"
                try:
                    text = fetch_page(url)
                    rows = read_year_value_csv_text(text)
                    self.stdout.write(f"Fetched {len(rows)} points for {spec['series_key']} from {url}")
                except Exception as exc:
                    self.stderr.write(
                        self.style.WARNING(f"{url} failed ({exc}); falling back to {path}")
                    )

            if not rows:
                rows = read_year_value_csv(path)

            for year, value in rows:
                bulk.append(
                    DepartmentMetric(
                        series_key=spec["series_key"],
                        year=year,
                        value=value,
                    )
                )

        DepartmentMetric.objects.bulk_create(bulk)
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(bulk)} DepartmentMetric rows."))
