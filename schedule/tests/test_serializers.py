import datetime
import pytest

from schedule.models import Schedule, SchoolClass, Teacher, Subject
from schedule.serializers import ScheduleSerializer


@pytest.fixture
def schedule() -> Schedule:
    schedule = Schedule(
        school_class=SchoolClass(
            name="5A",
        ),
        subject=Subject(
            name="Math",
            teacher=Teacher(
                name="Alex",
            ),
        ),
        dow=7,
        hour=datetime.time(hour=8)
    )
    # The next line emulates the .annotate, which works poorly with mypy
    schedule.class_student_count = 23   # type: ignore
    return schedule


def test_serialize_example(snapshot, schedule: Schedule):
    serializer = ScheduleSerializer(instance=schedule)
    snapshot.assert_match(serializer.data)
