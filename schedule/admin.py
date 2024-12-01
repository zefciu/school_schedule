from django.contrib import admin

from schedule.models import SchoolClass, Subject, Teacher, Student, Schedule

admin.site.register(SchoolClass)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Schedule)

# Register your models here.
