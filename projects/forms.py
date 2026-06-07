from django import forms

from .models import Project
from users.mixins import GithubURLValidationMixin


class ProjectForm(GithubURLValidationMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'required_skills']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'required_skills': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
