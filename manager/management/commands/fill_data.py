import random
from django.core.management.base import BaseCommand
from faker import Faker
from manager.models import Task, TaskType, Worker, Position, Team, Project

fake = Faker()

class Command(BaseCommand):
    help = "Generate random data for the database"

    def handle(self, *args, **kwargs):
        self.create_positions()
        self.create_teams_and_workers()
        self.create_task_types()
        self.create_projects_and_tasks()

    def create_positions(self):
        positions = ["Developer", "Designer", "Manager", "Tester", "Support"]
        for position_name in positions:
            Position.objects.get_or_create(name=position_name)
        self.stdout.write(self.style.SUCCESS(f"Created {len(positions)} positions"))

    def create_teams_and_workers(self):
        # Create Teams and assign Workers
        for _ in range(10):  # Create 10 teams
            team_lead = self.create_worker()
            team = Team.objects.create(
                name=fake.company(),
                slogan=fake.catch_phrase(),
                team_lead=team_lead
            )

            # Create workers and assign to the team
            for _ in range(5):  # Each team has 5 workers
                worker = self.create_worker(team=team)
                worker.team = team
                worker.save()

            self.stdout.write(self.style.SUCCESS(f"Created team: {team.name} with 5 workers"))

    def create_worker(self, team=None):
        # Create a Worker with random Position
        position = Position.objects.order_by("?").first()
        worker = Worker.objects.create_user(
            username=fake.user_name(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            position=position,
            team=team
        )
        worker.set_password("password123")  # Set a default password
        worker.save()
        return worker

    def create_task_types(self):
        task_types = ["Development", "Design", "Testing", "Support", "Documentation"]
        for task_type_name in task_types:
            TaskType.objects.get_or_create(name=task_type_name)
        self.stdout.write(self.style.SUCCESS(f"Created {len(task_types)} task types"))

    def create_projects_and_tasks(self):
        workers = list(Worker.objects.all())
        task_types = list(TaskType.objects.all())
        teams = list(Team.objects.all())

        for _ in range(5):  # Create 5 projects
            project = Project.objects.create(
                name=fake.bs(),
                description=fake.text(),
                deadline=fake.date_between(start_date="today", end_date="+30d"),
                team=random.choice(teams),
                is_completed=random.choice([True, False])
            )

            # Assign participants to project
            participants = random.sample(workers, 5)  # Assign 5 random workers to project
            project.participants.set(participants)

            for _ in range(10):  # Each project has 10 tasks
                task = Task.objects.create(
                    name=fake.sentence(nb_words=4),
                    description=fake.text(),
                    deadline=fake.date_between(start_date="today", end_date="+30d"),
                    is_completed=random.choice([True, False]),
                    priority=random.randint(0, 3),
                    task_type=random.choice(task_types),
                    project=project
                )
                task.assignees.set(random.sample(workers, 2))  # Assign 2 random workers to task

            self.stdout.write(self.style.SUCCESS(f"Created project: {project.name} with 10 tasks"))
