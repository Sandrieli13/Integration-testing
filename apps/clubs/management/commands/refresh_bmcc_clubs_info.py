"""
Fetch public BMCC Student Activities / clubs pages and cache key text + links locally.

Run occasionally (e.g. after deploy or each semester):

    python manage.py refresh_bmcc_clubs_info
"""

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.clubs.bmcc_scraper import (
    DEFAULT_CLUBS_URL,
    scrape_bmcc_clubs_pages,
    scrape_result_to_model_dict,
)
from apps.clubs.models import BmccClubsInfo


class Command(BaseCommand):
    help = "Scrape BMCC student clubs / activities pages into BmccClubsInfo (id=1)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-join-page",
            action="store_true",
            help="Only fetch the main clubs directory page (faster).",
        )

    def handle(self, *args, **options):
        if options["skip_join_page"]:
            result = scrape_bmcc_clubs_pages(join_url=None)
        else:
            result = scrape_bmcc_clubs_pages()

        data = scrape_result_to_model_dict(result, DEFAULT_CLUBS_URL)
        data["fetched_at"] = timezone.now()

        obj, created = BmccClubsInfo.objects.update_or_create(
            pk=1,
            defaults=data,
        )

        if result.error and not result.intro_text:
            self.stderr.write(self.style.WARNING(f"Scrape reported issues: {result.error}"))
        else:
            verb = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{verb} BmccClubsInfo snapshot (pk=1)."))
