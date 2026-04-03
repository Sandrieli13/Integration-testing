"""Shared ordering and JSON helpers for career readiness pages (majors, skills, courses)."""

from __future__ import annotations

from careers.models import Major


# Display order in dropdowns; unknown majors sort alphabetically after these.
_MAJOR_ORDER: tuple[str, ...] = (
    "Computer Science AS",
    "Computer Information Systems AS",
    "Computer Network Technology AAS",
    "Multimedia Programming & Design AAS",
    "Data Science (A.S.)",
    "Data Science AS",  # legacy DB rows from older seeds
)


def majors_ordered() -> list[Major]:
    majors = list(Major.objects.all())
    order_map = {name: i for i, name in enumerate(_MAJOR_ORDER)}

    def sort_key(m: Major) -> tuple[int, str]:
        pos = order_map.get(m.major, len(_MAJOR_ORDER))
        return (pos, m.major.lower())

    majors.sort(key=sort_key)
    return majors


def major_skills_courses_map() -> dict[str, dict[str, list[int]]]:
    """For internship matcher: filter available skills/courses by major id (string keys for JSON)."""
    out: dict[str, dict[str, list[int]]] = {}
    for m in Major.objects.prefetch_related("skills", "courses").all():
        out[str(m.id)] = {
            "skill_ids": [s.id for s in m.skills.all()],
            "course_ids": [c.id for c in m.courses.all()],
        }
    return out
