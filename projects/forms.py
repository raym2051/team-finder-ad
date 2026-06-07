from django import forms

from .models import Project
from users.mixins import GithubURLValidationMixin


class ProjectForm(GithubURLValidationMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'skills']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'skills': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
