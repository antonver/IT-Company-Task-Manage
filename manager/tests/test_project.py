import random
from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from manager.forms import WorkerFilterForm
from manager.models import Worker, Team, Position, Project


class WorkerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(10):
            team_lead = Worker.objects.create_user(
                username=f"Team_lead_{i}", password="password123"
            )
            team = Team.objects.create(
                name=f"Team_{i}", slogan="Team is great", team_lead=team_lead
            )
            position = Position.objects.create(name=f"Position_{i}")
            Worker.objects.create_user(
                username=f"Worker_{i}",
                password="password123",
                team=team,
                position=position,
            )

        for i in range(10):
            project = Project.objects.create(
                name=f"Project_{i}",
                deadline=datetime(2024, 10, 17 + i, 14, 30),
                description="description",
                team=Team.objects.get(name=f"Team_{i}"),
                is_completed=random.choice([True, False]),
            )
            project.participants.set(Worker.objects.filter(username=f"Worker_{i}"))

    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="password123"
        )
        self.client.force_login(self.admin_user)

    def test_project_pagination(self):
        response = self.client.get(reverse("manager:project-list") + "?page=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["project_list"]), 5)

        response = self.client.get(reverse("manager:project-list") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["project_list"]), 5)

    def test_project_search_form(self):
        response = self.client.get(
            reverse("manager:project-list") + "?search-name=Project_1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["project_list"]), 1)

        response = self.client.get(
            reverse("manager:project-list") + "?search-name=nonexistent_project"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["project_list"]), 0)

    def test_project_filter_form(self):
        response = self.client.get(
            reverse("manager:project-list") + "?filter-deadline=2024-10-18"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["project_list"]), 1)

        response = self.client.get(
            reverse("manager:project-list") + "?filter-participants=2"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["project_list"]), 1)

        response = self.client.get(reverse("manager:project-list") + "?filter-team=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["project_list"]), 1)
