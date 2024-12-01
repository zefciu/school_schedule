import os
import pytest

from django.core.management import call_command

from schedule.models import SchoolClass, Teacher, Subject, Student, Schedule


DIR_PATH = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def test_data():
    call_command("loaddata", os.path.join(DIR_PATH, "test_data.json"))

    yield

    Schedule.objects.all().delete()
    Student.objects.all().delete()
    SchoolClass.objects.all().delete()
    Subject.objects.all().delete()
    Teacher.objects.all().delete()
