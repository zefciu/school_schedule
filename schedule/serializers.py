from django.db.models.sql import Query
from adrf.serializers import ModelSerializer
from rest_framework import serializers

from schedule.models import Schedule, SchoolClass


class ClassSerializer(ModelSerializer):
    class Meta:
        model=SchoolClass
        fields=["name"]

class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
        fields = ["class", "dow", "hour", "subject"]

    vars()["class"] = ClassSerializer(source="school_class")

    def to_representation(self, instance, *args, **kwargs):
        data = super().to_representation(instance, *args, **kwargs)
        data["class"]["student_count"] = instance.class_student_count
        return data



class QueryParamsSerializer(serializers.Serializer):
    class_name = serializers.CharField(required=True)
    for_today = serializers.BooleanField(required=False, default=False)