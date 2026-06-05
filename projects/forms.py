import re

from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

        def clean_github_url(self):
            url = self.cleaned_data.get("github_url")
            if url and not re.match(r'^https?://github\.com/', url):
                raise forms.ValidationError('Ссылка должна вести на GitHub')
            return url
