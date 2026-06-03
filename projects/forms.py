from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "github_url", "status"]
        labels = {
            "name": "Название",
            "description": "Описание",
            "github_url": "GitHub",
            "status": "Статус",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Например, Study Buddy"}),
            "description": forms.Textarea(
                attrs={
                    "rows": 6,
                    "placeholder": "Кого ищете, над чем работаете и чем можно помочь?",
                }
            ),
            "github_url": forms.URLInput(
                attrs={"placeholder": "https://github.com/team/project"}
            ),
        }
