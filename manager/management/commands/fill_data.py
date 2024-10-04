from django.core.management.base import BaseCommand
from faker import Faker
from manager.models import Task, TaskType, Worker, Position, Team, Project
from django.utils import timezone


class Command(BaseCommand):
    help = 'Fill the database with test data'

    def handle(self, *args, **kwargs):
        fake = Faker()


        for _ in range(5):
            Position.objects.create(name=fake.job())


        for _ in range(3):
            team_lead = Worker.objects.create_user(
                username=fake.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                position=Position.objects.order_by('?').first()
            )
            Team.objects.create(name=fake.company(), slogan=fake.catch_phrase(), team_lead=team_lead)


        for _ in range(10):
            Worker.objects.create_user(
                username=fake.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                position=Position.objects.order_by('?').first(),
                team=Team.objects.order_by('?').first()
            )


        for _ in range(5):
            TaskType.objects.create(name=fake.word())


        for _ in range(3):
            project = Project.objects.create(
                name=fake.company(),
                description=fake.text(),
                deadline=fake.future_date(),
                teams=Team.objects.order_by('?').first()
            )
            project.participants.set(Worker.objects.order_by('?')[:5])


        for _ in range(10):
            task = Task.objects.create(
                name=fake.word(),
                description=fake.text(),
                deadline=fake.future_date(),
                is_completed=fake.boolean(),
                priority=fake.random_element(elements=[0, 1, 2, 3]),
                task_type=TaskType.objects.order_by('?').first(),
                project=Project.objects.order_by('?').first()
            )
            task.assignees.set(Worker.objects.order_by('?')[:3])

        self.stdout.write(self.style.SUCCESS('Successfully filled the database with test data'))
