from django.core.management.base import BaseCommand
from manager.models import Task, TaskType, Worker, Position, Team, Project
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = "Fill the database with initial data"

    def handle(self, *args, **kwargs):

        Worker.objects.all().delete()
        Position.objects.all().delete()
        TaskType.objects.all().delete()
        Team.objects.all().delete()
        Project.objects.all().delete()


        position_dev = Position.objects.create(name="Developer")
        position_pm = Position.objects.create(name="Project Manager")
        position_tl = Position.objects.create(name="Team Lead")

        task_type_bug = TaskType.objects.create(name="Bug")
        task_type_feature = TaskType.objects.create(name="Feature")

        worker_3 = Worker.objects.create_user(
            username="johndoe2", password="password123", first_name="John", last_name="Doe", position=position_dev
        )
        # Создаем команду без team_lead
        team = Team.objects.create(name="Alpha", slogan="Teamwork makes the dream work", team_lead=worker_3)

        worker_1 = Worker.objects.create_user(
            username="johndoe1", password="password123", first_name="John", last_name="Doe", position=position_dev, team=team
        )
        worker_2 = Worker.objects.create_user(
            username="janedoe1", password="password123", first_name="Jane", last_name="Doe", position=position_pm, team=team
        )

        team.team_lead = worker_2
        team.save()

        project = Project.objects.create(
            name="Website Redesign",
            description="Redesign the company website",
            deadline=timezone.now() + timedelta(days=30),
            team=team,
        )
        project.participants.set([worker_1, worker_2])

        task_1 = Task.objects.create(
            name="Fix login bug",
            description="Fix the login issue with invalid credentials.",
            deadline=timezone.now() + timedelta(days=7),
            priority=2,
            task_type=task_type_bug,
            project=project,
        )
        task_1.assignees.set([worker_1])

        task_2 = Task.objects.create(
            name="Add user profile feature",
            description="Implement user profiles for the website.",
            deadline=timezone.now() + timedelta(days=14),
            priority=1,
            task_type=task_type_feature,
            project=project,
        )
        task_2.assignees.set([worker_2])

        self.stdout.write(self.style.SUCCESS("Data successfully loaded."))
