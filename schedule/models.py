from django.db import models
from django.db.models import ForeignKey

from schedule.const import DayOfWeek


class Named(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract=True



class SchoolClass(Named):
    pass


class Teacher(Named):
    pass


class Student(Named):
    school_class = models.ForeignKey(
        SchoolClass,
        related_name="students",
        on_delete=models.CASCADE,
    )


class Subject(Named):
    teacher = ForeignKey(
        Teacher,
        related_name="subjects",
        on_delete=models.CASCADE,
    )




class Schedule(models.Model):
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    dow = models.IntegerField(choices=DayOfWeek)
    hour = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(name="class_slot", fields=["school_class", "dow", "hour"]),
            models.UniqueConstraint(name="subject_slot", fields=["subject", "dow", "hour"]),
        ]
