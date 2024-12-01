import itertools
import random
from datetime import time

from django.db import transaction

from schedule.models import SchoolClass, Teacher, Subject, Student, Schedule

class_names = [
    f"{grade}{division}"
    for grade in range(1, 4)
    for division in ["Iron", "Steel", "Tin", "Pewter"]
]


FIRST_NAMES = [
    "Allrianne",
    "Antillus",
    "Aradan",
    "Ardous",
    "Ashweather",
    "Augustin",
    "Aving",
    "Bastien",
    "Callins",
    "Chapmot",
    "Dorise",
    "Dowser",
    "Dupon",
    "Edgard",
    "Edwarn",
    "Lesan",
    "Maraga",
    "Reshelle",
    "Trevva",
]

LAST_NAMES = [
    "Ahlstrom",
    "Barrington",
    "Cett",
    "Dagouter",
    "Davenpleu",
    "Delouse",
    "Elariel",
    "Geffenry",
    "Grimes",
    "Hammondess",
    "Heviers",
    "Innate",
    "Ladrian",
    "Liese",
    "Mecant",
    "Melstrom",
    "Shezler",
    "Shores",
    "Tarcsel",
    "Terrisborn",
    "Venture",
    "Yomen",
]

SUBJECTS = [
    "Maths",
    "Metalurgy",
    "Physics",
    "Terris Language",
    "Malwish Language",
    "High Imperial Language",
    "History - classic",
    "History - empire",
    "History - post-catacendre",
    "Hemalurgic biology",
    "Biology",
    "Applied theology",
    "Metallic arts",
    "Investiture sciences",
    "Physical education",
    "Cosmereology",
]

def get_names(n: int, taken=None) -> set[str]:
    taken = taken or set()
    res = set()
    for _ in range(n):
        while True:
            teacher_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
            if teacher_name not in res | taken:
                res.add(teacher_name)
                break
    return res




def run():
    with transaction.atomic():
        teacher_names = get_names(len(SUBJECTS))
        teachers = Teacher.objects.bulk_create(
            [Teacher(name=teacher_name) for teacher_name in teacher_names]
        )
        subjects = Subject.objects.bulk_create(
            [
                Subject(name=subject_name, teacher=teacher)
                for subject_name, teacher in zip(SUBJECTS, teachers)
            ]
        )
        student_names = get_names(160, teacher_names)
        student_to_class = {
            student_name: class_name
            for class_name, student_name in zip(itertools.cycle(class_names), student_names)
        }
        classes = SchoolClass.objects.bulk_create([
            SchoolClass(name=class_name)
            for class_name in class_names
        ])
        class_name_to_class = {school_class.name: school_class for school_class in classes}
        Student.objects.bulk_create([
            Student(
                name=student_name,
                school_class=class_name_to_class[student_to_class[student_name]]
            )
            for student_name in student_names
        ])
        schedules = []
        for dow in range(1, 6):
            for hour in range(8, 16):
                random.shuffle(subjects)
                class_to_subject = zip(classes, subjects)
                schedules += [
                    Schedule(
                        school_class=school_class,
                        subject=subject,
                        dow=dow,
                        hour=time(hour=hour)
                    ) for school_class, subject
                    in class_to_subject
                ]
        Schedule.objects.bulk_create(schedules)




run()
