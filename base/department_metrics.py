"""BMCC CIS / CS / CNT time-series used on DataAnalysisPage (CSV + ORM)."""

import csv
import os

from django.conf import settings

# Display order: Computer Science first, then department totals, then other majors.
CHART_DEFINITIONS = [
    {
        "series_key": "cs-enrollment",
        "title": "Computer Science — enrollment (headcount)",
        "csv": "csv/Enrollment data for CS Major.csv",
    },
    {
        "series_key": "cs-graduation",
        "title": "Computer Science — degrees awarded (completions)",
        "csv": "csv/Graduation data for CS major.csv",
    },
    {
        "series_key": "cis-dept-enrollment",
        "title": "CIS department — total enrollment",
        "csv": "csv/Enrollment data for CIS department.csv",
    },
    {
        "series_key": "cis-dept-graduation",
        "title": "CIS department — degrees awarded (completions)",
        "csv": "csv/Graduation data for CIS department.csv",
    },
    {
        "series_key": "cis-major-enrollment",
        "title": "Computer Information Systems (A.A.S.) — enrollment",
        "csv": "csv/Enrollment data for CIS Major.csv",
    },
    {
        "series_key": "cis-major-graduation",
        "title": "Computer Information Systems (A.A.S.) — degrees awarded",
        "csv": "csv/Graduation data for CIS major.csv",
    },
    {
        "series_key": "cnt-enrollment",
        "title": "Computer Network Technology — enrollment",
        "csv": "csv/Enrollment data for CNT Major.csv",
    },
    {
        "series_key": "cnt-graduation",
        "title": "Computer Network Technology — degrees awarded",
        "csv": "csv/Graduation data for CNT major.csv",
    },
]

ENROLLMENT_CHART_DEFINITIONS = [
    s for s in CHART_DEFINITIONS if s["series_key"].endswith("-enrollment")
]


def static_csv_abspath(relative_csv: str) -> str:
    return os.path.join(settings.STATICFILES_DIRS[0], relative_csv)


def read_year_value_csv(csv_path: str) -> list[list[int]]:
    """Read year,count rows. Lines that are not two integers (e.g. a header) are skipped."""
    rows: list[list[int]] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) < 2:
                continue
            try:
                rows.append([int(row[0]), int(row[1])])
            except ValueError:
                continue
    return rows
