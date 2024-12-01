from enum import IntEnum, auto

from django.db import models
from django.template.defaulttags import autoescape


class DayOfWeek(models.IntegerChoices):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7
