from constants import MIN_PASSWORD_LENGTH
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from core.mixins import GithubURLValidationMixin

User = get_user_model()


class CustomUserCreationForm(GithubURLValidationMixin, UserCreationForm):
    """Форма создания пользователя"""

    class Meta:
        model = User
        fields = ("username", "email", "github_url", "password1", "password2")

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if len(password) < MIN_PASSWORD_LENGTH:
            raise forms.ValidationError(
                f"Пароль должен содержать минимум {MIN_PASSWORD_LENGTH} символов"
            )
        return password
