from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import UserManager

from team_finder.constants import (
    PHONE_MAX_LENGTH,
    USER_NAME_MAX_LENGTH,
    USER_SURNAME_MAX_LENGTH,
)

from .service import generate_avatar


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
    phone = models.CharField("телефон", max_length=PHONE_MAX_LENGTH, blank=True)
    github_url = models.URLField("GitHub", blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    objects = UserManager()

    def save(self, *args, **kwargs):
        # Проверяем, изменилось ли имя (только для существующего пользователя)
        name_changed = False

        if self.pk:
            try:
                old = User.objects.get(pk=self.pk)
                if old.name != self.name or old.surname != self.surname:
                    name_changed = True
            except User.DoesNotExist:
                pass

        # Если имя изменилось — обновляем аватарку
        if name_changed and self.pk:
            if self.avatar:
                self.avatar.delete(save=False)

            full_name = f"{self.name} {self.surname}".strip()
            name_for_avatar = full_name if full_name else self.email or "User"

            avatar_file = generate_avatar(name_for_avatar)
            if avatar_file:
                self.avatar.save(avatar_file.name, avatar_file, save=False)

        # Создание нового пользователя
        if not self.pk and not self.avatar:
            full_name = f"{self.name} {self.surname}".strip()
            name_for_avatar = full_name if full_name else self.email or "User"

            avatar_file = generate_avatar(name_for_avatar)
            if avatar_file:
                self.avatar.save(avatar_file.name, avatar_file, save=False)

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-date_joined"]
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return f"{self.name} {self.surname}".strip() or self.email
