import datetime
from dataclasses import dataclass
from typing import Any

from asgiref.sync import sync_to_async
from django.db.models import QuerySet, Count
from django.http import QueryDict

from schedule.models import Schedule
from schedule.serializers import ScheduleSerializer, QueryParamsSerializer
from schedule.types import ScheduleQueryParams as ScheduleQueryParamsProtocol


async def get_schedule(params: ScheduleQueryParamsProtocol) -> "QuerySet[Schedule]":
    kwargs: dict[str, Any] = {"school_class__name": params.class_name}
    if params.dow:
        kwargs["dow"] = params.dow
    return Schedule.objects.filter(**kwargs)\
        .annotate(class_student_count=Count("school_class__students"))\
        .all()


async def serialize_schedules(schedules: QuerySet[Schedule]):
    return await sync_to_async(lambda: ScheduleSerializer(schedules, many=True).data)()


@dataclass
class ScheduleQueryParams(ScheduleQueryParamsProtocol):
    class_name: str
    dow: int | None


def get_params(params: QueryDict) -> ScheduleQueryParams:
    serializer = QueryParamsSerializer(data=params)
    serializer.is_valid(raise_exception=True)
    if serializer.validated_data["for_today"]:
        dow = datetime.date.today().weekday() + 1    # ISO convention
    else:
        dow = None
    return ScheduleQueryParams(
        class_name=serializer.validated_data["class_name"],
        dow=dow,
    )


def get_schedules_cache_key(params: ScheduleQueryParams) -> str:
    return f"schedules-{params.class_name}-{params.dow}"
