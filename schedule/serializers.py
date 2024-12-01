from adrf.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.fields import IntegerField

from schedule.models import Schedule, SchoolClass, Teacher, Subject


class TeacherSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["name"]


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = ["name"]


class ClassSerializer(ModelSerializer):
    class Meta:
        model = SchoolClass
        fields = ["name"]


class ScheduleSerializer(ModelSerializer):

    class Meta:
        model = Schedule
        fields = ["class", "day_of_week", "hour", "subject", "teacher"]

    day_of_week = IntegerField(source="dow")
    vars()["class"] = ClassSerializer(source="school_class")
    teacher = TeacherSerializer(source="subject.teacher")
    subject = SubjectSerializer()

    def to_representation(self, instance, *args, **kwargs):
        data = super().to_representation(instance, *args, **kwargs)
        data["class"]["student_count"] = instance.class_student_count
        return data


class QueryParamsSerializer(serializers.Serializer):
    class_name = serializers.CharField(required=True)
    for_today = serializers.BooleanField(required=False, default=False)
