"""BMCC CIS / CS / CNT time-series used on DataAnalysisPage (CSV + ORM)."""

import csv
import io
import os

from django.conf import settings

# Display order: Computer Science first, then department totals, then other majors.
# Chart titles are student-facing; methodological notes live on the DataAnalysis page.
CHART_DEFINITIONS = [
    {
        "series_key": "cs-enrollment",
        "title": "Computer Science (A.S.) — enrollment",
        "csv": "csv/Enrollment data for CS Major.csv",
    },
    {
        "series_key": "cs-graduation",
        "title": "Computer Science (A.S.) — degrees awarded",
        "csv": "csv/Graduation data for CS major.csv",
    },
    {
        "series_key": "cis-dept-enrollment",
        "title": "CIS department — total enrollment",
        "csv": "csv/Enrollment data for CIS department.csv",
    },
    {
        "series_key": "cis-dept-graduation",
        "title": "CIS department — degrees awarded",
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
        "title": "Computer Network Technology (A.A.S.) — enrollment",
        "csv": "csv/Enrollment data for CNT Major.csv",
    },
    {
        "series_key": "cnt-graduation",
        "title": "Computer Network Technology (A.A.S.) — degrees awarded",
        "csv": "csv/Graduation data for CNT major.csv",
    },
    {
        "series_key": "dsm-enrollment",
        "title": "Data Science (A.S.) — enrollment",
        "csv": "csv/Enrollment data for Data Science Major.csv",
    },
]

ENROLLMENT_CHART_DEFINITIONS = [
    s for s in CHART_DEFINITIONS if s["series_key"].endswith("-enrollment")
]

GRADUATION_CHART_DEFINITIONS = [
    s for s in CHART_DEFINITIONS if s["series_key"].endswith("-graduation")
]


def static_csv_abspath(relative_csv: str) -> str:
    return os.path.join(settings.STATICFILES_DIRS[0], relative_csv)


def read_year_value_rows(rows) -> list[list[int]]:
    """Parse year,count pairs. Non-numeric rows (e.g. headers) are skipped."""
    out: list[list[int]] = []
    for row in rows:
        if len(row) < 2:
            continue
        try:
            out.append([int(row[0]), int(row[1])])
        except ValueError:
            continue
    return out


def read_year_value_csv(csv_path: str) -> list[list[int]]:
    """Read year,count rows from a UTF-8 file on disk."""
    with open(csv_path, newline="", encoding="utf-8") as f:
        return read_year_value_rows(csv.reader(f))


def read_year_value_csv_text(text: str) -> list[list[int]]:
    """Same as read_year_value_csv but from an in-memory CSV string (e.g. HTTP body)."""
    return read_year_value_rows(csv.reader(io.StringIO(text)))
