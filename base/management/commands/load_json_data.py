import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from base.models import Courses, Majors, Semester


class Command(BaseCommand):
    help = 'Load data from JSON file (Majors, Courses, Semester)'

    @staticmethod
    def _course_ref(course_pk):
        if course_pk is None:
            return None
        return Courses.objects.get(course_id=course_pk)

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'base', 'fixtures', 'sql_code.json')

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        majors_data = data['Majors']
        courses_data = data['Courses']
        semester_data = data['Semester']

        for major in majors_data:
            Majors.objects.update_or_create(
                major_id=major['major_id'],
                defaults={'major_name': major['major_name']},
            )

        for course in courses_data:
            Courses.objects.update_or_create(
                course_id=course['course_id'],
                defaults={
                    'course_name': course['course_name'],
                    'major_id': course['major_id'],
                    'credits': course['credits'],
                },
            )

        for semester in semester_data:
            if semester.get('course6') is not None:
                self.stdout.write(
                    self.style.WARNING(
                        'Ignoring course6 in fixture (model has at most 5 courses per semester).'
                    )
                )
            major = Majors.objects.get(pk=semester['major_id'])
            Semester.objects.update_or_create(
                semester_id=semester['semester_id'],
                major=major,
                defaults={
                    'course1': self._course_ref(semester.get('course1')),
                    'course2': self._course_ref(semester.get('course2')),
                    'course3': self._course_ref(semester.get('course3')),
                    'course4': self._course_ref(semester.get('course4')),
                    'course5': self._course_ref(semester.get('course5')),
                    'total_credits': semester['total_credits'],
                },
            )

        self.stdout.write(self.style.SUCCESS('Data loaded successfully.'))
