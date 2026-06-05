from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from team_finder.constants import ITEMS_PER_PAGE
from team_finder.pagination import paginate_queryset

from .forms import EmailLoginForm, ProfileEditForm, RegisterForm, UserPasswordChangeForm
from .models import User


def register(request):
    if request.user.is_authenticated:
        return redirect("projects:project_list")

    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Аккаунт создан. Теперь можно войти.")
        return redirect("users:login")

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("projects:project_list")

    form = EmailLoginForm(request, data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect(request.GET.get("next") or "projects:project_list")

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("projects:project_list")


def profile_detail(request, user_id):
    profile = get_object_or_404(
        User.objects.prefetch_related(
            "owned_projects__participants",
            "owned_projects__skills",
        ),
        pk=user_id,
    )
    return render(request, "users/user-details.html", {"user": profile})


@login_required
def edit_profile(request):
    form = ProfileEditForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user,
    )
    if form.is_valid():
        form.save()
        messages.success(request, "Профиль обновлён.")
        return redirect("users:profile_detail", user_id=request.user.id)

    return render(
        request,
        "users/edit_profile.html",
        {"form": form, "user": request.user},
    )


def participants_list(request):
    queryset = User.objects.order_by("-date_joined")
    page_obj = paginate_queryset(request, queryset, ITEMS_PER_PAGE)
    return render(
        request,
        "users/participants.html",
        {
            "participants": page_obj,
            "page_obj": page_obj,
        },
    )


@login_required
def change_password(request):
    form = UserPasswordChangeForm(request.user, request.POST or None)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Пароль изменён.")
        return redirect("users:profile_detail", user_id=request.user.id)

    return render(request, "users/change_password.html", {"form": form})
