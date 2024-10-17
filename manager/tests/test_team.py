from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from manager.forms import TeamFilterForm
from manager.models import Team, Position, Project, Worker


class TeamTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.team_lead1 = Worker.objects.create_user(
            username="lead_1", password="password123"
        )

        for i in range(10):
            Team.objects.create(
                name=f"Team_{i}",
                slogan="Beta Slogan",
                team_lead=Worker.objects.create(
                    username=f"worker_{i}", password="password123"
                ),
            )

        cls.position1 = Position.objects.create(name="Developer")
        cls.position2 = Position.objects.create(name="Manager")

        cls.project1 = Project.objects.create(
            name="Project Alpha", deadline="2024-12-31", team=Team.objects.first()
        )
        cls.project2 = Project.objects.create(
            name="Project Beta", deadline="2024-11-30", team=Team.objects.first()
        )

    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="password123"
        )
        self.client.force_login(self.admin_user)

    def test_team_pagination(self):
        response = self.client.get(reverse("manager:team-list") + "?page=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["team_list"]), 5)

    def test_team_search_form(self):
        response = self.client.get(reverse("manager:team-list") + "?search-name=Team_1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["team_list"]), 1)

        response = self.client.get(
            reverse("manager:team-list") + "?search-name=Nonexistent Team"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["team_list"]), 0)

    def test_team_filter_form(self):
        response = self.client.get(reverse("manager:team-list") + "?project=1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["team_list"]), 1)

        response = self.client.get(reverse("manager:team-list") + "?project=10")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["team_list"]), 0)
