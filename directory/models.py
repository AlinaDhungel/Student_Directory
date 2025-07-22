from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=50)
    faculty = models.CharField(max_length=100)
    section = models.CharField(max_length=50)
    semester = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"
