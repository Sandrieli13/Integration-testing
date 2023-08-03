import json 
import os
from django.core.management.base import BaseCommand
from base.models import Majors, Courses, Semester

class Command(BaseCommand):
    help = 'Load data from JSON file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join('base', 'fixtures', 'sql_code.json')

        with open(file_path, 'r') as file:
            data = json.load(file)

            majors_data = data['Majors']
            courses_data = data['Courses']
            semester_data = data['Semester']

            # Load Majors data
            for major in majors_data:
                Majors.objects.create(
                    major_id=major['major_id'],
                    major_name=major['major_name']
                )

            # Load Courses data
            for course in courses_data:
                Courses.objects.create(
                    course_id=course['course_id'],
                    course_name=course['course_name'],
                    major_id=course['major_id'],
                    credits=course['credits']
                )

            # Load Semester data
            for semester in semester_data:
                Semester.objects.create(
                    semester_id=semester['semester_id'],
                    major_id=semester['major_id'],
                    course1_id=semester['course1'],
                    course2_id=semester['course2'],
                    course3_id=semester['course3'],
                    course4_id=semester['course4'],
                    course5_id=semester['course5'],
                    course6_id=semester['course6'],
                    total_credits=semester['total_credits']
                )

        self.stdout.write(self.style.SUCCESS('Data loaded successfully.'))
