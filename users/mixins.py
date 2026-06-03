"""Миксины для переиспользования в формах"""

from django import forms
from django.users.exceptions import ValidationError
from django.users.validators import URLValidator


class GithubURLValidationMixin:
    """Миксин для валидации GitHub URL"""

    def clean_github_url(self):
        github_url = self.cleaned_data.get("github_url")

        if not github_url:
            return github_url

        # Валидация URL
        url_validator = URLValidator()
        try:
            url_validator(github_url)
        except ValidationError:
            raise forms.ValidationError("Введите корректный URL")

        # Проверка, что это GitHub URL
        if "github.com" not in github_url.lower():
            raise forms.ValidationError("URL должен быть ссылкой на GitHub")

        return github_url
