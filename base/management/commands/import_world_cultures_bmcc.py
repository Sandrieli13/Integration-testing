from django.core.management.base import BaseCommand

from base.bmcc_pathway_scrape import fetch_and_parse
from base.models import WorldCulturesAndGlobalIssues

DEFAULT_URL = (
    "https://www.bmcc.cuny.edu/academics/pathways/world-cultures-and-global-issues/"
)


class Command(BaseCommand):
    help = (
        "Fetch BMCC World Cultures and Global Issues courses from the college site "
        "and replace rows in WorldCulturesAndGlobalIssues."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            default=DEFAULT_URL,
            help="Page URL to scrape (default: BMCC Pathways WC&GI list).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse and print count only; do not change the database.",
        )

    def handle(self, *args, **options):
        url = options["url"]
        dry_run = options["dry_run"]

        try:
            rows = fetch_and_parse(url)
        except RuntimeError as e:
            self.stderr.write(self.style.ERROR(str(e)))
            raise SystemExit(1) from e

        if dry_run:
            self.stdout.write(self.style.SUCCESS(f"Parsed {len(rows)} courses (dry run)."))
            return

        WorldCulturesAndGlobalIssues.objects.all().delete()
        WorldCulturesAndGlobalIssues.objects.bulk_create(
            [
                WorldCulturesAndGlobalIssues(
                    credit=credit,
                    course_name=course_name,
                    description=description,
                )
                for credit, course_name, description in rows
            ]
        )
        self.stdout.write(
            self.style.SUCCESS(f"Loaded {len(rows)} World Cultures and Global Issues courses.")
        )
