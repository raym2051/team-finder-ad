"""Модели пользователей и аватаров"""

from constants import (
    MAX_EMAIL_LENGTH,
    MAX_GITHUB_URL_LENGTH,
    MAX_NAME_LENGTH,
    MAX_USERNAME_LENGTH,
)
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from core.managers import UserManager
from core.service import generate_avatar


class User(AbstractUser):
    """Кастомная модель пользователя"""

    username = models.CharField(max_length=MAX_USERNAME_LENGTH, unique=True)
    email = models.EmailField(max_length=MAX_EMAIL_LENGTH, unique=True)
    first_name = models.CharField(max_length=MAX_NAME_LENGTH, blank=True)
    last_name = models.CharField(max_length=MAX_NAME_LENGTH, blank=True)
    github_url = models.URLField(max_length=MAX_GITHUB_URL_LENGTH, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    objects = UserManager()

    class Meta:
        ordering = ["username"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Генерируем аватарку при создании, если ее нет
        if not self.avatar and not self.pk:
            avatar_file = generate_avatar(self.username)
            self.avatar.save(avatar_file.name, avatar_file, save=False)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:user_detail", args=[self.username])
