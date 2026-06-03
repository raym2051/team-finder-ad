from http import HTTPStatus

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from team_finder.constants import ITEMS_PER_PAGE

from .models import User


class UserFlowTests(TestCase):
    def test_user_can_register_and_then_login_by_email(self):
        register_response = self.client.post(
            reverse("users:register"),
            {
                "name": "Ника",
                "surname": "Морозова",
                "email": "nika@example.com",
                "password": "review-pass-123",
            },
        )

        self.assertRedirects(register_response, reverse("users:login"))
        self.assertTrue(User.objects.filter(email="nika@example.com").exists())

        login_response = self.client.post(
            reverse("users:login"),
            {
                "email": "nika@example.com",
                "password": "review-pass-123",
            },
        )

        self.assertRedirects(login_response, reverse("projects:project_list"))

    def test_participants_list_is_paginated_by_twelve_users(self):
        for index in range(ITEMS_PER_PAGE + 1):
            User.objects.create_user(
                email=f"user{index}@example.com",
                password="pass",
                name=f"User {index}",
                surname="Tester",
            )

        response = self.client.get(reverse("users:participants_list"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context["participants"]), ITEMS_PER_PAGE)
        self.assertTrue(response.context["page_obj"].has_next())

    def test_seed_demo_creates_users_with_projects(self):
        call_command("seed_demo", verbosity=0)

        demo_users = User.objects.filter(email__endswith="@teamfinder.local")

        self.assertGreaterEqual(demo_users.count(), 4)
        for user in demo_users:
            self.assertGreaterEqual(user.owned_projects.count(), 1)
