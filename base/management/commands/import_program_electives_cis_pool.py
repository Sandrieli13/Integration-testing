"""
Load the CIS/CSC/GIS program-elective pool into ProgramElectives.

Requirement text (degree rule, not a single course): students choose courses from
this list until they have earned 6 credits (e.g. two 3-credit courses, or one
4-credit and one 3-credit course, depending on selections).

Data is pulled from BMCC listings; GIS 201 is filled from the college catalog
when it does not appear on those pages.
"""

from urllib.error import URLError

from django.core.management.base import BaseCommand

from base.bmcc_pathway_scrape import fetch_page, parse_department_course_listing
from base.models import ProgramElectives

URL_CIS = (
    "https://www.bmcc.cuny.edu/academics/departments/cis/"
    "course-listings/computer-information-systems/"
)
URL_CSC = (
    "https://www.bmcc.cuny.edu/academics/departments/cis/"
    "course-listings/computer-science-courses/"
)

# Same order as typical degree wording; all must resolve after merge + manual.
POOL_CODES = [
    "CIS 317",
    "CIS 345",
    "CIS 359",
    "CIS 362",
    "CIS 364",
    "CIS 385",
    "CIS 395",
    "CSC 103",
    "GIS 201",
    "CIS 316",
    "CIS 272",
    "CIS 285",
    "CSC 203",
]

# https://bmcc.catalog.cuny.edu/courses/1236101
_GIS_201 = (
    4,
    "GIS 201 — Introduction to Geographic Methods",
    (
        "This course introduces the means by which geographers analyze the world "
        "to better understand geography and geographical processes. It teaches "
        "the students various methods for interpreting and analyzing spatial data "
        "including cartography, Geographic Information Systems (GIS), remote "
        "sensing, spatial statistics and survey research."
    ),
)


class Command(BaseCommand):
    help = (
        "Replace ProgramElectives with the CIS/CSC/GIS pool (6 credits to be "
        "chosen from these courses). Fetches CIS and CSC listings from BMCC."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Fetch and validate only; do not change the database.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        try:
            merged = parse_department_course_listing(fetch_page(URL_CIS))
            merged.update(parse_department_course_listing(fetch_page(URL_CSC)))
        except URLError as e:
            self.stderr.write(self.style.ERROR(f"Failed to fetch BMCC listings: {e}"))
            raise SystemExit(1) from e

        merged["GIS 201"] = _GIS_201

        rows: list[tuple[int, str, str]] = []
        missing: list[str] = []
        for code in POOL_CODES:
            if code not in merged:
                missing.append(code)
                continue
            rows.append(merged[code])

        if missing:
            self.stderr.write(
                self.style.ERROR(
                    "Missing from BMCC listings / manual data: " + ", ".join(missing)
                )
            )
            raise SystemExit(1)

        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Resolved {len(rows)} program elective courses (dry run)."
                )
            )
            return

        ProgramElectives.objects.all().delete()
        ProgramElectives.objects.bulk_create(
            [
                ProgramElectives(
                    credit=credit,
                    course_name=course_name,
                    description=description,
                )
                for credit, course_name, description in rows
            ]
        )
        self.stdout.write(
            self.style.SUCCESS(f"Loaded {len(rows)} program elective pool courses.")
        )
