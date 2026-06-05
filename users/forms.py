import re

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm

from .models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Минимум 6 символов"}),
    )

    class Meta:
        model = User
        fields = '__all__'

    def clean_github_url(self):
        url = self.cleaned_data.get("github_url")
        if url and not re.match(r'^https?://github\.com/', url):
            raise forms.ValidationError('Ссылка должна вести на GitHub')
        return url

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class EmailLoginForm(forms.Form):
    email = forms.EmailField(
        label="Имейл",
        widget=forms.EmailInput(attrs={"placeholder": "alice@example.com"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Ваш пароль"}),
    )

    error_messages = {
        "invalid_login": "Проверьте имейл и пароль.",
        "inactive": "Этот аккаунт отключён.",
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(
                self.request,
                username=email,
                password=password,
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages["invalid_login"],
                    code="invalid_login",
                )
            if not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages["inactive"],
                    code="inactive",
                )

        return cleaned_data

    def get_user(self):
        return self.user_cache


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["avatar", "name", "surname", "about", "phone", "github_url"]
        widgets = {
            "avatar": forms.FileInput(attrs={"class": "avatar-input"}),
            "about": forms.Textarea(attrs={"rows": 5}),
            "phone": forms.TextInput(attrs={"placeholder": "+7 900 000-00-00"}),
            "github_url": forms.URLInput(attrs={"placeholder": "https://github.com/username"}),
        }

    def clean_github_url(self):
        url = self.cleaned_data.get("github_url")
        if url and not re.match(r'^https?://github\.com/', url):
            raise forms.ValidationError('Ссылка должна вести на GitHub')
        return url


class UserPasswordChangeForm(PasswordChangeForm):
    pass
