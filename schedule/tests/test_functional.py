import pytest
from freezegun import freeze_time


@pytest.mark.usefixtures("transactional_db", "test_data")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("dow", "expected_schedules"),
    [
        pytest.param(2, 8, id="tuesday"),
        pytest.param(None, 40, id="all_week"),
    ]
)
@freeze_time("2024-11-29")  # A Friday
async def test_get_schedules(async_client, snapshot, dow: int | None, expected_schedules: int):
    response = await async_client.get("/schedule/?class_name=1Iron")
    snapshot.assert_match(response.json())
