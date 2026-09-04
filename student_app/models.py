from django.db import models
from django.contrib.auth.models import User

class ClassGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    mark = models.IntegerField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )

    class_group = models.ForeignKey(
        ClassGroup,
        on_delete=models.SET_NULL,
        related_name="students",
        null=True,
        blank=True
    )

    subjects = models.ManyToManyField(
        Subject,
        related_name="students",
        blank=True
    )

    is_top_performer = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.name