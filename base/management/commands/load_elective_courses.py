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
        "Load pathway / program elective tables from base/fixtures/elective_courses.json "
        "(no network; use on PythonAnywhere where BMCC scrape commands may be blocked)."
    )

    def handle(self, *args, **kwargs):
        path = os.path.join(settings.BASE_DIR, "base", "fixtures", "elective_courses.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        IndividualAndSociety.objects.all().delete()
        IndividualAndSociety.objects.bulk_create(
            [
                IndividualAndSociety(
                    credit=row["credit"],
                    course_name=row["course_name"],
                    description=row["description"],
                )
                for row in data["IndividualAndSociety"]
            ]
        )

        USExperienceInItsDiversity.objects.all().delete()
        USExperienceInItsDiversity.objects.bulk_create(
            [
                USExperienceInItsDiversity(
                    credit=row["credit"],
                    course_name=row["course_name"],
                    description=row["description"],
                )
                for row in data["USExperienceInItsDiversity"]
            ]
        )

        WorldCulturesAndGlobalIssues.objects.all().delete()
        WorldCulturesAndGlobalIssues.objects.bulk_create(
            [
                WorldCulturesAndGlobalIssues(
                    credit=row["credit"],
                    course_name=row["course_name"],
                    description=row["description"],
                )
                for row in data["WorldCulturesAndGlobalIssues"]
            ]
        )

        ProgramElectives.objects.all().delete()
        ProgramElectives.objects.bulk_create(
            [
                ProgramElectives(
                    credit=row["credit"],
                    course_name=row["course_name"],
                    description=row["description"],
                )
                for row in data["ProgramElectives"]
            ]
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Elective tables loaded: "
                f"I&S {len(data['IndividualAndSociety'])}, "
                f"US {len(data['USExperienceInItsDiversity'])}, "
                f"WC {len(data['WorldCulturesAndGlobalIssues'])}, "
                f"PE {len(data['ProgramElectives'])}."
            )
        )
