"""
Load majors, jobs, skills, courses, and sample internships for the career readiness tools.

Usage:
  python manage.py seed_careers_data --reset      # recommended: wipe careers_* tables then load
  python manage.py seed_careers_data              # upsert-like: refresh links / descriptions by name
  python manage.py seed_careers_data --reset --scrape   # optional BMCC department HTML blurb (needs network)

Curated graph: careers/seed_dataset.py. Chart payloads: careers/tech_market_charts.py.
"""

from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from careers.models import Course, Intern, Job, Major, Skill
from careers.scrapers.bmcc_mcs import excerpt_for_context, fetch_department_page_text
from careers import seed_dataset as SD


def _truncate(s: str, n: int) -> str:
    s = (s or "").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


class Command(BaseCommand):
    help = "Seed careers DB for majors/jobs/skills pages, skills gaps, and internship matcher."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete all Intern, Major, Job, Course, Skill rows before loading.",
        )
        parser.add_argument(
            "--scrape",
            action="store_true",
            help="Fetch BMCC Math/CS department HTML (best effort); appends excerpt to first major description.",
        )

    def handle(self, *args, **options):
        scrape_note = None
        if options["scrape"]:
            self.stdout.write("Optional: fetching BMCC department page…")
            page = fetch_department_page_text()
            scrape_note = excerpt_for_context(page)

        with transaction.atomic():
            if options["reset"]:
                self.stdout.write(self.style.WARNING("Clearing careers tables…"))
                Intern.objects.all().delete()
                Major.objects.all().delete()
                Job.objects.all().delete()
                Course.objects.all().delete()
                Skill.objects.all().delete()

            skill_map: dict[str, Skill] = {}
            for name, gap in SD.SKILLS:
                obj, _ = Skill.objects.update_or_create(name=name, defaults={"gapfiller": gap})
                skill_map[name] = obj

            course_map: dict[str, Course] = {}
            for name in SD.COURSES:
                obj, _ = Course.objects.get_or_create(name=name)
                course_map[name] = obj

            job_map: dict[str, Job] = {}
            for title_raw, skill_names in SD.JOBS:
                title = _truncate(title_raw, 100)
                job, _ = Job.objects.get_or_create(job_title=title)
                job.skills.set([skill_map[s] for s in skill_names if s in skill_map])
                job.save()
                job_map[title_raw] = job
                job_map[title] = job

            for idx, mj in enumerate(SD.MAJORS):
                title = _truncate(mj["major"], 100)
                desc = (mj.get("description") or "").strip()
                if idx == 0 and scrape_note:
                    desc = (desc + "\n\n— BMCC Mathematics & Computer Science (live page excerpt):\n" + scrape_note).strip()

                major, _ = Major.objects.update_or_create(
                    major=title,
                    defaults={"description": desc[:2000]},
                )
                major.skills.set([skill_map[s] for s in mj["skills"] if s in skill_map])
                major.courses.set([course_map[c] for c in mj["courses"] if c in course_map])
                job_objs = []
                for j in mj["jobs"]:
                    key = j if j in job_map else _truncate(j, 100)
                    if key in job_map:
                        job_objs.append(job_map[key])
                major.jobs_From_Bmcc.set(job_objs)
                major.save()

            for row in SD.INTERNS:
                t = _truncate(row["title"], 200)
                link = row["link"].strip()
                if not link.startswith("http"):
                    link = "https://" + link
                link = link[:200]

                intern = Intern.objects.filter(title=t).first()
                if intern is None:
                    intern = Intern(title=t, link=link, description="")
                intern.description = (row.get("description") or "")[:4000]
                intern.link = link
                intern.save()
                intern.skills.set([skill_map[s] for s in row["skills"] if s in skill_map])
                intern.courses.set([course_map[c] for c in row["courses"] if c in course_map])
                intern.save()

        # One-time cleanup: older seeds used "Data Science AS"; canonical label is now "Data Science (A.S.)".
        if Major.objects.filter(major="Data Science (A.S.)").exists():
            Major.objects.filter(major="Data Science AS").delete()

        self.stdout.write(self.style.SUCCESS("Careers seed complete."))
        self.stdout.write(f"  Skills: {Skill.objects.count()}")
        self.stdout.write(f"  Courses: {Course.objects.count()}")
        self.stdout.write(f"  Jobs: {Job.objects.count()}")
        self.stdout.write(f"  Majors: {Major.objects.count()}")
        self.stdout.write(f"  Internships: {Intern.objects.count()}")
