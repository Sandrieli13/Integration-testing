from django.core.management.base import BaseCommand

from base.bmcc_pathway_scrape import fetch_and_parse
from base.models import USExperienceInItsDiversity

DEFAULT_URL = (
    "https://www.bmcc.cuny.edu/academics/pathways/u-s-experience-in-its-diversity/"
)


class Command(BaseCommand):
    help = (
        "Fetch BMCC U.S. Experience in its Diversity courses and replace rows in "
        "USExperienceInItsDiversity."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            default=DEFAULT_URL,
            help="Page URL to scrape (default: BMCC Pathways US Experience list).",
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

        USExperienceInItsDiversity.objects.all().delete()
        USExperienceInItsDiversity.objects.bulk_create(
            [
                USExperienceInItsDiversity(
                    credit=credit,
                    course_name=course_name,
                    description=description,
                )
                for credit, course_name, description in rows
            ]
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Loaded {len(rows)} U.S. Experience in its Diversity courses."
            )
        )
