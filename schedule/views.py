# Create your views here.
from adrf.views import APIView
from django.core.cache import cache
from rest_framework.response import Response

from schedule.types import (
    ScheduleGetter,
    SchedulesSerializingService,
    ScheduleQueryParamsGetter,
    ScheduleCacheKeyGenerator,
)


class SchedulesView(APIView):

    get_schedule: ScheduleGetter | None = None
    serialize_schedules: SchedulesSerializingService | None = None
    get_query_params: ScheduleQueryParamsGetter | None = None
    get_cache_key: ScheduleCacheKeyGenerator | None = None

    async def get(
            self,
            request,

    ):
        query_params = self.get_query_params(request.query_params)
        cache_key = self.get_cache_key(query_params)
        if (data := (await cache.aget(cache_key))) is None:
            schedules = await self.get_schedule(
                query_params
            )
            data = await self.serialize_schedules(schedules)
            await cache.aset(cache_key, data)
        return Response(data)
