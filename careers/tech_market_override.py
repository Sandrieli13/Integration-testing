"""
Optional local file for tech career stats (openings + wages) from any vetted source.

Use when BLS Public Data API has not yet published your target year, or you prefer
figures copied from OEWS data tables / another official extract.

Place JSON at:  <BASE_DIR>/data/tech_career_stats_override.json  (gitignored)

Disable with env:  TECH_CAREER_STATS_OVERRIDE_DISABLE=1
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_tech_career_stats_override(path: Path) -> tuple[list[dict], list[dict], str, str, str] | None:
    """
    Returns (openings, salary, oews_year, geo_note, source_name) or None if invalid.

    JSON shape:
      {
        "version": 1,
        "source_name": "BLS OEWS national tables, May 2025",
        "oews_year": "2025",
        "geo_note": "United States, national",
        "openings": [{"label": "Software Developers", "y": 1500000}],
        "salary": [{"y": 72.5, "label": "Software Developers"}]
      }
    Labels in openings and salary must match for the scatter chart.
    """
    try:
        with open(path, encoding="utf-8") as f:
            data: dict[str, Any] = json.load(f)
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return None

    if data.get("version") != 1:
        return None

    openings = data.get("openings")
    salary = data.get("salary")
    if not isinstance(openings, list) or not isinstance(salary, list):
        return None
    if len(openings) < 1 or len(salary) < 1:
        return None

    year = str(data.get("oews_year") or "").strip() or "—"
    geo = str(data.get("geo_note") or "Custom data file").strip()
    source = str(data.get("source_name") or "Local override file").strip()

    for row in openings:
        if not isinstance(row, dict) or "label" not in row or "y" not in row:
            return None
        try:
            row["y"] = int(round(float(row["y"])))
        except (TypeError, ValueError):
            return None

    for row in salary:
        if not isinstance(row, dict) or "label" not in row or "y" not in row:
            return None
        try:
            row["y"] = round(float(row["y"]), 2)
        except (TypeError, ValueError):
            return None

    return openings, salary, year, geo, source
