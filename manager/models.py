from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ForeignKey


class Task(models.Model):
    priority = [(0, 'Low'), (1, 'Medium'), (2, 'High'), (3, 'Very High')]
    name = models.CharField(max_length=255, blanc=False, null=False)
    description = models.TextField(blanc=False, null=False)
    deadline = models.DateField(blank=False, null=False)
    is_completed = models.BooleanField(default=False, null=False)
    priority = models.CharField(choices=priority, blank=False, null=False)
    task_type = models.ForeignKey("TaskType", on_delete=models.CASCADE)
    assignees = models.ManyToManyField("Worker", blank=False, null=False, related_name="assignees")


class TaskType(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)


class Worker(AbstractUser):
    position = models.ForeignKey("Position", on_delete=models.CASCADE)


class Position(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
