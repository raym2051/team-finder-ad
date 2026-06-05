from django.conf import settings
from django.db import models

from team_finder.constants import (
    PROJECT_NAME_MAX_LENGTH,
    SKILL_NAME_MAX_LENGTH,
    STATUS_MAX_LENGTH,
)


class Skill(models.Model):
    name = models.CharField(
        "название",
        max_length=SKILL_NAME_MAX_LENGTH,
        unique=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "навык"
        verbose_name_plural = "навыки"

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_OPEN = "open"
    STATUS_CLOSED = "closed"
    STATUS_CHOICES = (
        (STATUS_OPEN, "Открыт"),
        (STATUS_CLOSED, "Закрыт"),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="автор",
    )
    name = models.CharField("название", max_length=PROJECT_NAME_MAX_LENGTH)
    description = models.TextField("описание", blank=True)
    github_url = models.URLField("GitHub", blank=True)
    status = models.CharField(
        "статус",
        max_length=STATUS_MAX_LENGTH,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
    )
    skills = models.ManyToManyField(Skill, related_name="projects", blank=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participating_projects",
        blank=True,
    )
    created_at = models.DateTimeField("дата публикации", auto_now_add=True)
    updated_at = models.DateTimeField("дата обновления", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "проект"
        verbose_name_plural = "проекты"

    def __str__(self):
        return self.name
