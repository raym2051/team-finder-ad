"""Основные view-функции сайта"""

from http import HTTPStatus

from constants import PAGINATION_PAGE_SIZE
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render

from core.service import paginate_queryset

User = get_user_model()


def user_list(request):
    """
    Список пользователей с пагинацией
    """
    users = User.objects.all().order_by("username")
    paginator, page_obj = paginate_queryset(
        request, users, PAGINATION_PAGE_SIZE)

    return render(
        request,
        "core/user_list.html",
        {
            "page_obj": page_obj,
            "paginator": paginator,
        },
    )


def api_user_check(request):
    """
    API проверка существования пользователя
    """
    username = request.GET.get("username")

    if not username:
        return JsonResponse(
            {"error": "Username parameter required"}, status=HTTPStatus.BAD_REQUEST
        )

    exists = User.objects.filter(username=username).exists()

    return JsonResponse({"exists": exists}, status=HTTPStatus.OK)
