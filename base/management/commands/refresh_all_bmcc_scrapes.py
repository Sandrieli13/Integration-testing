"""
Run every BMCC-facing import (Pathways + CIS listings) and reload department metrics.

Pathways / department pages require outbound HTTP. On PythonAnywhere free tier, external
fetches are often blocked—use a paid account or run these locally and upload data.

Usage:
  python manage.py refresh_all_bmcc_scrapes
  python manage.py refresh_all_bmcc_scrapes --fetch-metrics   # needs BMCC_METRICS_CSV_BASE_URL
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Fetch BMCC Pathways and CIS elective listings, then sync department metrics "
        "(CSV files or optional HTTP mirror)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-pathways",
            action="store_true",
            help="Do not run Individual & Society, US Experience, World Cultures imports.",
        )
        parser.add_argument(
            "--skip-program-electives",
            action="store_true",
            help="Do not refresh CIS/CSC program-elective pool from department pages.",
        )
        parser.add_argument(
            "--skip-department-metrics",
            action="store_true",
            help="Do not run sync_department_metrics.",
        )
        parser.add_argument(
            "--fetch-metrics",
            action="store_true",
            help="Pass --fetch-from-web to sync_department_metrics (requires BMCC_METRICS_CSV_BASE_URL).",
        )

    def handle(self, *args, **options):
        if not options["skip_pathways"]:
            self.stdout.write("Importing Individual & Society…")
            call_command("import_individual_society_bmcc")
            self.stdout.write("Importing U.S. Experience…")
            call_command("import_us_experience_bmcc")
            self.stdout.write("Importing World Cultures…")
            call_command("import_world_cultures_bmcc")

        if not options["skip_program_electives"]:
            self.stdout.write("Importing CIS/CSC program electives pool…")
            call_command("import_program_electives_cis_pool")

        if not options["skip_department_metrics"]:
            self.stdout.write("Syncing department metrics (enrollment / graduation series)…")
            if options["fetch_metrics"]:
                call_command("sync_department_metrics", fetch_from_web=True)
            else:
                call_command("sync_department_metrics")

        self.stdout.write(self.style.SUCCESS("BMCC refresh finished."))
