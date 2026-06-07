from http import HTTPStatus
import json

from django.test import TestCase
from django.urls import reverse

from projects.models import Project, Skill
from users.models import User

from team_finder.constants import ITEMS_PER_PAGE

MISSING_OBJECT_ID = 999_999


class ProjectFlowTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@example.com",
            password="pass12345",
            name="Оля",
            surname="Командная",
        )
        self.member = User.objects.create_user(
            email="member@example.com",
            password="pass12345",
            name="Илья",
            surname="Разработчик",
        )

    def test_project_list_filters_by_required_skill_and_highlights_active_filter(self):
        django = Skill.objects.create(name="Django")
        react = Skill.objects.create(name="React")
        matching_project = Project.objects.create(
            owner=self.owner,
            name="Backend Hub",
            description="Сервис для учебных команд",
        )
        matching_project.skills.add(django)
        other_project = Project.objects.create(
            owner=self.owner,
            name="Frontend Lab",
            description="Интерфейс для дизайнеров",
        )
        other_project.skills.add(react)

        response = self.client.get(reverse("projects:project_list"), {"skill": "Django"})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Backend Hub")
        self.assertNotContains(response, "Frontend Lab")
        self.assertEqual(response.context["active_skill"], "Django")

    def test_project_list_is_paginated_by_twelve_projects(self):
        for index in range(ITEMS_PER_PAGE + 1):
            Project.objects.create(
                owner=self.owner,
                name=f"Project {index}",
                description="Описание",
            )

        response = self.client.get(reverse("projects:project_list"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context["projects"]), ITEMS_PER_PAGE)
        self.assertTrue(response.context["page_obj"].has_next())

    def test_owner_can_create_and_remove_project_skill_without_reload(self):
        project = Project.objects.create(
            owner=self.owner,
            name="Skill Board",
            description="Команда для прототипов",
        )
        self.client.force_login(self.owner)

        add_response = self.client.post(
            reverse("projects:add_project_skill", args=[project.id]),
            data=json.dumps({"name": "FastAPI"}),
            content_type="application/json",
        )

        self.assertEqual(add_response.status_code, HTTPStatus.OK)
        skill = Skill.objects.get(name="FastAPI")
        self.assertTrue(project.skills.filter(id=skill.id).exists())

        remove_response = self.client.post(reverse("projects:remove_project_skill", args=[project.id, skill.id]))

        self.assertEqual(remove_response.status_code, HTTPStatus.OK)
        self.assertFalse(project.skills.filter(id=skill.id).exists())

    def test_non_owner_cannot_change_project_skills(self):
        project = Project.objects.create(
            owner=self.owner,
            name="Protected Board",
            description="Описание",
        )
        skill = Skill.objects.create(name="PostgreSQL")
        self.client.force_login(self.member)

        response = self.client.post(
            reverse("projects:add_project_skill", args=[project.id]),
            data=json.dumps({"skill_id": skill.id}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertFalse(project.skills.filter(id=skill.id).exists())

    def test_json_project_actions_return_json_404_for_missing_project(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("projects:add_project_skill", args=[MISSING_OBJECT_ID]),
            data=json.dumps({"name": "Django"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.json()["error"], "project_not_found")

    def test_json_skill_actions_return_json_404_for_missing_skill(self):
        project = Project.objects.create(
            owner=self.owner,
            name="Skill Board",
            description="Команда для прототипов",
        )
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse(
                "projects:remove_project_skill",
                args=[project.id, MISSING_OBJECT_ID],
            )
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.json()["error"], "skill_not_found")

    def test_authenticated_user_can_join_and_leave_other_project(self):
        project = Project.objects.create(
            owner=self.owner,
            name="Open Team",
            description="Описание",
        )
        self.client.force_login(self.member)

        join_response = self.client.post(reverse("projects:toggle_participate", args=[project.id]))

        self.assertEqual(join_response.status_code, HTTPStatus.OK)
        self.assertTrue(project.participants.filter(id=self.member.id).exists())
        self.assertTrue(join_response.json()["participant"])

        leave_response = self.client.post(reverse("projects:toggle_participate", args=[project.id]))

        self.assertEqual(leave_response.status_code, HTTPStatus.OK)
        self.assertFalse(project.participants.filter(id=self.member.id).exists())
        self.assertFalse(leave_response.json()["participant"])
