from django.urls import path

from schedule.services import get_schedule, get_params, serialize_schedules, get_schedules_cache_key
from schedule.views import SchedulesView

urlpatterns = [
    path("", SchedulesView.as_view(
        get_schedule=get_schedule,
        get_query_params=get_params,
        get_cache_key=get_schedules_cache_key,
        serialize_schedules=serialize_schedules,
    ), name="schedules")
]