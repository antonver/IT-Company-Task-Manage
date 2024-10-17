from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from manager.models import Task, TaskType, Worker, Project, Team
from datetime import date


class TaskTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.team = Team.objects.create(
            name="Team Alpha",
            slogan="Teamwork makes the dream work",
            team_lead=Worker.objects.create_user(
                username="john_doe_",
                password="password123",
            ),
        )

        # Create a TaskType
        cls.task_type = TaskType.objects.create(name="Bug Fix")

        # Create a Worker
        cls.worker = Worker.objects.create_user(
            username="john_doe",
            password="password123",
        )

        cls.project = Project.objects.create(
            name="Project Alpha",
            deadline=date(2024, 12, 31),
            description="Project description",
            team=cls.team,
            is_completed=False,
        )

        # Create multiple tasks for pagination and search tests
        for i in range(30):
            task = Task.objects.create(
                name=f"Task_{i}",
                description=f"Description for task {i}",
                deadline=date(2024, 12, 31),
                is_completed=(i % 2 == 0),
                priority=(i % 4),
                task_type=cls.task_type,
                project=cls.project,
            )
            task.assignees.add(cls.worker)

    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(self.worker)
        self.client.force_login(self.admin_user)

    def test_task_pagination(self):
        response = self.client.get(reverse("manager:task-list") + "?page=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["task_list"]), 5)

        response = self.client.get(reverse("manager:task-list") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["task_list"]), 5)

        response = self.client.get(reverse("manager:task-list") + "?page=3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["task_list"]), 5)

    def test_task_search_form(self):
        response = self.client.get(
            reverse("manager:task-list") + "?search-name=Task_29"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["task_list"]), 1)

        response = self.client.get(
            reverse("manager:task-list") + "?search-name=Non-existent Task"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["task_list"]), 0)

    def test_task_filter_form(self):
        response = self.client.get(
            reverse("manager:task-list") + "?filter-is_completed=true"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            all(task.is_completed for task in response.context["task_list"])
        )

        response = self.client.get(reverse("manager:task-list") + "?filter-priority=1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            all(task.priority == 1 for task in response.context["task_list"])
        )

        response = self.client.get(
            reverse("manager:task-list") + f"?filter-project={self.project.id}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            all(task.project == self.project for task in response.context["task_list"])
        )

        response = self.client.get(
            reverse("manager:task-list") + f"?filter-task_type={self.task_type.id}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            all(
                task.task_type == self.task_type
                for task in response.context["task_list"]
            )
        )

        response = self.client.get(
            reverse("manager:task-list") + f"?filter-assignees={self.worker.id}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            all(
                self.worker in task.assignees.all()
                for task in response.context["task_list"]
            )
        )
