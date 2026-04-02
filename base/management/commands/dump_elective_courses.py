import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from base.models import (
    IndividualAndSociety,
    ProgramElectives,
    USExperienceInItsDiversity,
    WorldCulturesAndGlobalIssues,
)


class Command(BaseCommand):
    help = (
        "Write IndividualAndSociety, USExperienceInItsDiversity, "
        "WorldCulturesAndGlobalIssues, and ProgramElectives to "
        "base/fixtures/elective_courses.json (for load_elective_courses / PA)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--stdout",
            action="store_true",
            help="Print JSON to stdout instead of writing the fixture file.",
        )

    def handle(self, *args, **options):
        data = {
            "IndividualAndSociety": list(
                IndividualAndSociety.objects.order_by("id").values(
                    "credit", "course_name", "description"
                )
            ),
            "USExperienceInItsDiversity": list(
                USExperienceInItsDiversity.objects.order_by("id").values(
                    "credit", "course_name", "description"
                )
            ),
            "WorldCulturesAndGlobalIssues": list(
                WorldCulturesAndGlobalIssues.objects.order_by("id").values(
                    "credit", "course_name", "description"
                )
            ),
            "ProgramElectives": list(
                ProgramElectives.objects.order_by("id").values(
                    "credit", "course_name", "description"
                )
            ),
        }

        text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"

        if options["stdout"]:
            self.stdout.write(text)
            return

        path = os.path.join(settings.BASE_DIR, "base", "fixtures", "elective_courses.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

        self.stdout.write(
            self.style.SUCCESS(
                f"Wrote {path} — I&S {len(data['IndividualAndSociety'])}, "
                f"US {len(data['USExperienceInItsDiversity'])}, "
                f"WC {len(data['WorldCulturesAndGlobalIssues'])}, "
                f"PE {len(data['ProgramElectives'])}."
            )
        )
