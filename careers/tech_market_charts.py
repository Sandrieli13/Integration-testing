"""
Chart payloads for the tech career statistics page (CanvasJS).

These figures are intended for student exploration:
- "Openings" and "pay" are illustrative, derived from typical NYC-scale magnitudes
- language shares are survey-style (not required to sum to 100%)

For production-grade stats, wire up official data pulls (BLS/OEWS, Census, etc.).
"""

from __future__ import annotations


def get_tech_career_chart_series() -> tuple[list[dict], list[dict], list[dict], dict, list[dict]]:
    """
    Returns (openings_pie, salary_spline, languages_column, meta, scatter_pay_vs_openings).

    CanvasJS expectations:
    - pie uses {label, y}
    - spline/column uses {y, label}
    - scatter uses {x, y, label}
    """

    # Illustrative job counts (NYC-scale magnitudes; not a live BLS pull)
    openings = [
        {"label": "Software Developers", "y": 19800},
        {"label": "Computer Systems Analysts", "y": 12400},
        {"label": "Information Security Analysts", "y": 4200},
        {"label": "Web & Digital Interface Designers", "y": 3100},
        {"label": "Database Administrators", "y": 2100},
        {"label": "Computer Network Architects", "y": 2800},
        {"label": "Data Scientists (subset SOC)", "y": 3600},
    ]

    # Illustrative median hourly wages (USD/hr)
    salary = [
        {"y": 72, "label": "Software Developers"},
        {"y": 58, "label": "Computer Systems Analysts"},
        {"y": 64, "label": "Information Security Analysts"},
        {"y": 52, "label": "Web & Digital Interface Designers"},
        {"y": 56, "label": "Database Administrators"},
        {"y": 67, "label": "Computer Network Architects"},
        {"y": 61, "label": "Data Scientists (subset SOC)"},
    ]

    # Survey-style language shares (%), sum not required to be 100
    languages = [
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

    openings_sorted = sorted(openings, key=lambda d: d["y"], reverse=True)
    top_openings = openings_sorted[:3]

    top_languages = sorted(languages, key=lambda d: d["y"], reverse=True)[:5]

    salary_values = [d["y"] for d in salary]
    salary_min = min(salary_values) if salary_values else 0
    salary_max = max(salary_values) if salary_values else 0
    top_paid = max(salary, key=lambda d: d["y"]) if salary else None

    # Scatter: median pay vs openings for occupations that exist in both series
    openings_by_label = {d["label"]: d["y"] for d in openings}
    scatter_points = []
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

    meta = {
        "openings_note": "Illustrative NYC-scale counts for selected computing occupations (for planning, not job guarantees).",
        "salary_note": "Illustrative median hourly wages; verify on BLS OEWS and current postings.",
        "languages_note": "Survey-style language shares (not required to sum to 100%).",
        "as_of": "2025-Q2 snapshot (update tech_market_charts.py as sources publish new tables).",
        "insights": {
            "top_roles_openings": top_openings,
            "salary_range": {"min": salary_min, "max": salary_max},
            "top_paid": top_paid,
            "top_languages": top_languages,
            "learning_tracks": learning_tracks,
        },
    }

    return openings, salary, languages, meta, scatter_points
