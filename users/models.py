from django.contrib.auth.models import AbstractUser
from django.db import models

from team_finder.constants import (
    PHONE_MAX_LENGTH,
    USER_NAME_MAX_LENGTH,
    USER_SURNAME_MAX_LENGTH,
)
from users.managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField("email", unique=True)
    name = models.CharField("имя", max_length=USER_NAME_MAX_LENGTH)
    surname = models.CharField("фамилия", max_length=USER_SURNAME_MAX_LENGTH)
    avatar = models.ImageField(
        "аватар",
        upload_to="avatars/",
        blank=True,
        null=True,
    )
    about = models.TextField("о себе", blank=True)
    phone = models.CharField(
        "телефон",
        max_length=PHONE_MAX_LENGTH,
        blank=True
    )
    github_url = models.URLField("GitHub", blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    objects = UserManager()

    class Meta:
        ordering = ["-date_joined"]
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return f"{self.name} {self.surname}".strip() or self.email
