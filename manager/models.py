from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Task(models.Model):
    PRIORITY_CHOICES = [(0, "Low"), (1, "Medium"), (2, "High"), (3, "Very High")]
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    deadline = models.DateField(blank=False, null=False)
    is_completed = models.BooleanField(default=False, null=False)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, blank=False, null=False)
    task_type = models.ForeignKey("TaskType", on_delete=models.CASCADE, related_name="tasks")
    assignees = models.ManyToManyField(
        "Worker", blank=False, null=False, related_name="tasks"
    )
    project = models.ForeignKey("Project", on_delete=models.CASCADE, blank=True, null=True, related_name="tasks")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class TaskType(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey("Position", on_delete=models.CASCADE, related_name="workers", null=True, blank=True)
    team = models.ForeignKey("Team", on_delete=models.CASCADE, related_name="workers", null=True, blank=True)

    class Meta(AbstractUser.Meta):
        verbose_name = "worker"
        verbose_name_plural = "workers"
        ordering = ["position"]

    def __str__(self):
        return f"{self.position}: {self.last_name} {self.first_name}"

    def get_absolute_url(self):
        return reverse("manager:worker-detail", kwargs={"pk":self.pk})


class Position(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    slogan = models.CharField(max_length=255, blank=False, null=False)
    team_lead = models.OneToOneField(Worker, on_delete=models.CASCADE, related_name="team_lead")

    def __str__(self):
        return self.name


class Project(models.Model):
    deadline = models.DateField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    participants = models.ManyToManyField("Worker", related_name="projects")
    team = models.ForeignKey("Team", on_delete=models.CASCADE, related_name="projects")
    is_completed = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.name
