import pytest

from schedule.services import ScheduleQueryParams, get_schedule


@pytest.mark.usefixtures("transactional_db", "test_data")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("dow", "expected_schedules"),
    [
        pytest.param(2, 8, id="tuesday"),
        pytest.param(None, 40, id="all_week"),
    ]
)
async def test_get_schedules(dow: int | None, expected_schedules: int):
    params = ScheduleQueryParams(class_name="1Iron", dow=dow)
    schedule_qs = await get_schedule(params)
    schedules = [schedule async for schedule in schedule_qs]
    assert len(schedules) == expected_schedules
