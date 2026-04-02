from django.core.management.base import BaseCommand
from django.db import transaction

from base.department_metrics import CHART_DEFINITIONS, read_year_value_csv, static_csv_abspath
from base.models import DepartmentMetric


class Command(BaseCommand):
    help = (
        "Load DepartmentMetric rows from static CSV files (same source as the data analysis charts). "
        "Run after deploy or when CSV values change."
    )

    @transaction.atomic
    def handle(self, *args, **options):
        DepartmentMetric.objects.all().delete()
        bulk = []
        for spec in CHART_DEFINITIONS:
            path = static_csv_abspath(spec["csv"])
            for year, value in read_year_value_csv(path):
                bulk.append(
                    DepartmentMetric(
                        series_key=spec["series_key"],
                        year=year,
                        value=value,
                    )
                )
        DepartmentMetric.objects.bulk_create(bulk)
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(bulk)} DepartmentMetric rows."))
