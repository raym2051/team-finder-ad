from http import HTTPStatus

from constants import PAGINATION_PAGE_SIZE, PROJECT_STATUS_CLOSED
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render

from core.service import get_skills_autocomplete, paginate_queryset
from projects.forms import ProjectForm
from projects.models import Project


def project_list(request):
    """
    Список проектов с оптимизированными запросами
    """
    # Оптимизация: select_related для автора, prefetch_related для участников
    projects = (
        Project.objects.select_related("author") .prefetch_related(
            Prefetch(
                "participants",
                queryset=Project.participants.only("id")),
            "skills") .all())

    # Пагинация через общую функцию
    paginator, page_obj = paginate_queryset(
        request, projects, PAGINATION_PAGE_SIZE)

    context = {
        "page_obj": page_obj,
        "paginator": paginator,
    }
    return render(request, "projects/project_list.html", context)


@login_required
def project_create(request):
    """
    Создание проекта
    """
    # Используем request.POST or None для унификации обработки
    form = ProjectForm(request.POST or None)

    if form.is_valid():  # request.method == 'POST' проверяется внутри
        project = form.save(commit=False)
        project.author = request.user
        project.save()
        form.save_m2m()  # сохраняем many-to-many связи
        messages.success(request, "Проект успешно создан!")
        return redirect("projects:project_detail", project.id)

    return render(request, "projects/project_form.html", {"form": form})


@login_required
def project_join(request, project_id):
    """
    Вступление в проект
    """
    project = get_object_or_404(Project, id=project_id)

    # Оптимизированная проверка через exists()
    if not project.participants.filter(id=request.user.id).exists():
        project.participants.add(request.user)
        messages.success(request, f'Вы вступили в проект "{project.title}"')
    else:
        messages.warning(request, "Вы уже участвуете в этом проекте")

    return redirect("projects:project_detail", project_id)


@login_required
def project_leave(request, project_id):
    """
    Выход из проекта
    """
    project = get_object_or_404(Project, id=project_id)

    if project.participants.filter(id=request.user.id).exists():
        project.participants.remove(request.user)
        messages.success(request, f'Вы вышли из проекта "{project.title}"')

    return redirect("projects:project_detail", project_id)


@login_required
def project_close(request, project_id):
    """
    Закрытие проекта (только для автора)
    """
    project = get_object_or_404(Project, id=project_id, author=request.user)

    if project.status != PROJECT_STATUS_CLOSED:
        project.close()  # используем метод модели с константой
        messages.success(request, "Проект закрыт")

    return redirect("projects:project_detail", project_id)


def skills_autocomplete(request):
    """
    AJAX автокомплит для навыков
    """
    query = request.GET.get("q", "")
    skills = get_skills_autocomplete(query)

    # Возвращаем JSON с правильным HTTP статусом
    data = [{"id": skill.id, "name": skill.name} for skill in skills]

    from django.http import JsonResponse

    return JsonResponse(data, safe=False, status=HTTPStatus.OK)
