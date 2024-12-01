from typing import Protocol, Any

from django.db.models import QuerySet

from schedule.models import Schedule


class ScheduleQueryParams(Protocol):
    class_name: str
    for_today: bool


class ScheduleGetter(Protocol):
    async def __call__(self, query_params: ScheduleQueryParams) -> QuerySet[Schedule]:
        ...


class SchedulesSerializingService(Protocol):
    async def __call__(self, services: QuerySet[Schedule]) -> Any:
        ...


class ScheduleQueryParamsGetter(Protocol):
    def __call__(self, args: Any) -> ScheduleQueryParams:
        ...

class ScheduleCacheKeyGenerator(Protocol):
    async def __call__(self, params: ScheduleQueryParams) -> str:
        ...

