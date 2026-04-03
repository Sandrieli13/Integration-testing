"""
Chart payloads for the tech career statistics page (CanvasJS).

When BLS_API_KEY is set, openings and median hourly pay are loaded from the U.S. Bureau
of Labor Statistics OEWS API (cached on disk). Language shares stay survey-style static data.
"""

from __future__ import annotations

from pathlib import Path

from django.conf import settings

# Survey-style; unchanged when switching to live BLS for openings/wages.
_LANGUAGES_STATIC: list[dict] = [
    {"y": 62.0, "label": "JavaScript / TypeScript"},
    {"y": 54.0, "label": "HTML / CSS"},
    {"y": 51.0, "label": "SQL"},
    {"y": 49.0, "label": "Python"},
    {"y": 30.0, "label": "Java"},
    {"y": 28.0, "label": "C#"},
    {"y": 22.0, "label": "C++"},
    {"y": 18.0, "label": "PHP"},
    {"y": 14.0, "label": "Go"},
    {"y": 9.0, "label": "Rust"},
    {"y": 8.0, "label": "Ruby"},
    {"y": 7.0, "label": "Swift"},
    {"y": 12.0, "label": "Shell / CLI"},
]


def _scatter_from(openings: list[dict], salary: list[dict]) -> list[dict]:
    openings_by_label = {d["label"]: d["y"] for d in openings}
    scatter_points: list[dict] = []
    for s in salary:
        label = s["label"]
        if label in openings_by_label:
            scatter_points.append(
                {
                    "x": s["y"],
                    "y": openings_by_label[label],
                    "label": label,
                }
            )
    return scatter_points


def _meta_bundle(
    openings: list[dict],
    salary: list[dict],
    languages: list[dict],
    *,
    live_oews: bool,
    oews_year: str | None,
    geo_note: str | None,
) -> dict:
    openings_sorted = sorted(openings, key=lambda d: d["y"], reverse=True)
    top_openings = openings_sorted[:3]

    top_languages = sorted(languages, key=lambda d: d["y"], reverse=True)[:5]

    salary_values = [d["y"] for d in salary]
    salary_min = min(salary_values) if salary_values else 0
    salary_max = max(salary_values) if salary_values else 0
    top_paid = max(salary, key=lambda d: d["y"]) if salary else None

    learning_tracks = [
        {
            "title": "Frontend / Web track",
            "description": "Target roles by building 2-3 portfolio projects: responsive UI, API integration, and deployment.",
            "bullets": ["HTML/CSS", "JavaScript/TypeScript", "REST APIs", "UI/UX basics"],
        },
        {
            "title": "Data track (analytics -> ML)",
            "description": "Start with SQL + Python notebooks, then publish one reproducible workflow (from question to dashboard).",
            "bullets": ["SQL", "Python", "Data analysis", "Machine learning intro"],
        },
        {
            "title": "Security / Ops track",
            "description": "Build confidence with labs: networks, Linux/CLI automation, and security fundamentals.",
            "bullets": ["Networking fundamentals", "Linux/CLI", "Cybersecurity awareness", "Technical writing"],
        },
    ]

    if live_oews and oews_year and geo_note:
        as_of = (
            f"OEWS {oews_year} · {geo_note}. "
            "BMCC offers an A.S. in Data Science (DSM-AS); align coursework with the Math department program sheet."
        )
        openings_note = (
            f"BLS OEWS employment ({oews_year}), same occupations as the chart — not job postings or guarantees."
        )
        salary_note = (
            f"BLS OEWS hourly median wage ({oews_year}). Confirm with OEWS tables and local job posts."
        )
    else:
        as_of = (
            "Illustrative planning snapshot (enable BLS_API_KEY for live OEWS). "
            "BMCC offers an A.S. in Data Science (DSM-AS); align coursework with the Math department program sheet."
        )
        openings_note = "Illustrative U.S.-scale counts for selected computing occupations (for planning, not job guarantees)."
        salary_note = "Illustrative median hourly wages; verify on BLS OEWS and current postings."

    return {
        "openings_note": openings_note,
        "salary_note": salary_note,
        "languages_note": "Survey-style language shares (not required to sum to 100%); not from BLS.",
        "as_of": as_of,
        "live_oews": live_oews,
        "oews_year": oews_year or "",
        "geo_note": geo_note or "",
        "insights": {
            "top_roles_openings": top_openings,
            "salary_range": {"min": salary_min, "max": salary_max},
            "top_paid": top_paid,
            "top_languages": top_languages,
            "learning_tracks": learning_tracks,
        },
    }


def get_tech_career_chart_series_static() -> tuple[list[dict], list[dict], list[dict], dict, list[dict]]:
    """Original illustrative series (no network)."""

    openings = [
        {"label": "Software Developers", "y": 19800},
        {"label": "Computer Systems Analysts", "y": 12400},
        {"label": "Information Security Analysts", "y": 4200},
        {"label": "Web & Digital Interface Designers", "y": 3100},
        {"label": "Database Administrators", "y": 2100},
        {"label": "Computer Network Architects", "y": 2800},
        {"label": "Data Scientists (subset SOC)", "y": 3600},
    ]

    salary = [
        {"y": 72, "label": "Software Developers"},
        {"y": 58, "label": "Computer Systems Analysts"},
        {"y": 64, "label": "Information Security Analysts"},
        {"y": 52, "label": "Web & Digital Interface Designers"},
        {"y": 56, "label": "Database Administrators"},
        {"y": 67, "label": "Computer Network Architects"},
        {"y": 61, "label": "Data Scientists (subset SOC)"},
    ]

    languages = list(_LANGUAGES_STATIC)

    scatter = _scatter_from(openings, salary)
    meta = _meta_bundle(
        openings,
        salary,
        languages,
        live_oews=False,
        oews_year=None,
        geo_note=None,
    )
    return openings, salary, languages, meta, scatter


def get_tech_career_chart_series() -> tuple[list[dict], list[dict], list[dict], dict, list[dict]]:
    """
    Prefer live BLS OEWS when BLS_API_KEY is set; otherwise illustrative static data.
    Cached under BASE_DIR/data/bls_tech_market_cache.json (see refresh_tech_career_bls command).
    """
    api_key = getattr(settings, "BLS_API_KEY", "") or ""
    metro = getattr(settings, "BLS_OEWS_METRO_AREA_CODE", "") or ""
    cache_hours = getattr(settings, "BLS_TECH_MARKET_CACHE_HOURS", 24)

    if api_key:
        from careers.bls_oews_client import load_or_fetch_tech_oews

        base = Path(settings.BASE_DIR)
        metro_code = metro if len(metro) == 7 and metro.isdigit() else None
        live = load_or_fetch_tech_oews(
            api_key,
            base,
            cache_hours=int(cache_hours),
            metro_area_code=metro_code,
            force_refresh=False,
        )
        if live:
            openings, salary, oews_year, geo_note = live
            languages = list(_LANGUAGES_STATIC)
            scatter = _scatter_from(openings, salary)
            meta = _meta_bundle(
                openings,
                salary,
                languages,
                live_oews=True,
                oews_year=oews_year,
                geo_note=geo_note,
            )
            return openings, salary, languages, meta, scatter

    return get_tech_career_chart_series_static()
