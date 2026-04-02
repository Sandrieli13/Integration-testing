# Tables for IndividualAndSociety and related models were missing from some DBs
# (e.g. sqlite file replaced after 0002 was already recorded). Recreate if absent.

from django.db import migrations


_CREATE = """
CREATE TABLE IF NOT EXISTS "Individual and Society" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "credit" integer NOT NULL,
    "course_name" varchar(255) NOT NULL,
    "description" text NOT NULL
);
CREATE TABLE IF NOT EXISTS "Program Electives" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "credit" integer NOT NULL,
    "course_name" varchar(255) NOT NULL,
    "description" text NOT NULL
);
CREATE TABLE IF NOT EXISTS "US Experience In ItsDiversity" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "credit" integer NOT NULL,
    "course_name" varchar(255) NOT NULL,
    "description" text NOT NULL
);
CREATE TABLE IF NOT EXISTS "World Cultures And GlobalIssues" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "credit" integer NOT NULL,
    "course_name" varchar(255) NOT NULL,
    "description" text NOT NULL
);
"""

_DROP = """
DROP TABLE IF EXISTS "World Cultures And GlobalIssues";
DROP TABLE IF EXISTS "US Experience In ItsDiversity";
DROP TABLE IF EXISTS "Program Electives";
DROP TABLE IF EXISTS "Individual and Society";
"""


def _apply(apps, schema_editor):
    if schema_editor.connection.vendor != 'sqlite':
        return
    with schema_editor.connection.cursor() as cursor:
        cursor.executescript(_CREATE)


def _unapply(apps, schema_editor):
    if schema_editor.connection.vendor != 'sqlite':
        return
    with schema_editor.connection.cursor() as cursor:
        cursor.executescript(_DROP)


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_semester_options'),
    ]

    operations = [
        migrations.RunPython(_apply, _unapply),
    ]
