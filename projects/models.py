"""Модели проектов и навыков"""

from constants import (
    MAX_PROJECT_DESCRIPTION_LENGTH,
    MAX_PROJECT_TITLE_LENGTH,
    PROJECT_STATUS_CHOICES,
    PROJECT_STATUS_CLOSED,
    PROJECT_STATUS_OPEN,
)
from django.conf import settings
from django.db import models
from django.urls import reverse


class Skill(models.Model):
    """Модель навыка"""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    """Модель проекта"""

    title = models.CharField(max_length=MAX_PROJECT_TITLE_LENGTH)
    description = models.TextField(max_length=MAX_PROJECT_DESCRIPTION_LENGTH)
    github_url = models.URLField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=PROJECT_STATUS_CHOICES,
        default=PROJECT_STATUS_OPEN)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_projects",
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participating_projects",
        blank=True)
    skills = models.ManyToManyField(Skill, related_name="projects", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projects:project_detail", args=[self.id])

    def is_participant(self, user):
        """Проверка, участвует ли пользователь в проекте (оптимизированная)"""
        if not user.is_authenticated:
            return False
        return self.participants.filter(id=user.id).exists()

    def close(self):
        """Закрыть проект"""
        self.status = PROJECT_STATUS_CLOSED
        self.save()
