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
            Worker.objects.create_user(
                username=f"Worker_{i}",
                password="password123",
                team=Team.objects.create(
                    name=f"Team_{i}",
                    slogan="Team is great",
                    team_lead=Worker.objects.create(
                        username=f"Team_lead_{i}", password="password123"
                    ),
                ),
                position=Position.objects.create(name=f"Position_{i}"),
            )
        projects = []
        for i in range(10):
            projects.append(
                Project.objects.create(
                    name=f"Project_{i}",
                    deadline=datetime(2024, 10, 17, 14, 30),
                    description="description",
                    team=Team.objects.order_by("?").first(),
                    is_completed=random.choice([True, False]),
                )
            )
            projects[i].participants.set(Worker.objects.filter(username=f"Worker_{i}"))

    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="password123"
        )
        self.client.force_login(self.admin_user)

    def test_worker_pagination(self):
        response = self.client.get(reverse("manager:worker-list") + "?page=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["worker_list"]), 5)

        response = self.client.get(reverse("manager:worker-list") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["worker_list"]), 5)

    def test_worker_search_form(self):
        response = self.client.get(
            reverse("manager:worker-list") + "?search-username=Worker_1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["worker_list"]), 1)

        response = self.client.get(
            reverse("manager:worker-list") + "?search-username=nonexistent_worker"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["worker_list"]), 0)

    def test_worker_filter_form(self):
        response = self.client.get(
            reverse("manager:worker-list") + "?filter-position=1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["worker_list"]), 1)

        response = self.client.get(reverse("manager:worker-list") + "?filter-team=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["worker_list"]), 1)

        response = self.client.get(
            reverse("manager:worker-list") + "?filter-projects=1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["worker_list"]), 1)
