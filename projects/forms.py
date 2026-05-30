from django import forms

from core.mixins import GithubURLValidationMixin
from projects.models import Project


class ProjectForm(GithubURLValidationMixin, forms.ModelForm):
    """Форма создания/редактирования проекта"""

    class Meta:
        model = Project
        fields = ["title", "description", "github_url", "skills"]
