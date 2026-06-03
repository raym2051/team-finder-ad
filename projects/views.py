from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from team_finder.constants import (
    ITEMS_PER_PAGE,
    SKILL_AUTOCOMPLETE_LIMIT,
    SKILL_NAME_MAX_LENGTH,
)
from team_finder.helpers import json_error, json_payload
from team_finder.pagination import paginate_queryset

from .forms import ProjectForm
from .models import Project, Skill


def project_list(request):
    active_skill = request.GET.get("skill", "").strip()
    queryset = (
        Project.objects.select_related("owner")
        .prefetch_related("participants", "skills")
        .order_by("-created_at")
    )

    if active_skill:
        queryset = queryset.filter(skills__name__iexact=active_skill)

    page_obj = paginate_queryset(request, queryset.distinct(), ITEMS_PER_PAGE)
    all_skills = Skill.objects.order_by("name").values_list("name", flat=True)

    return render(
        request,
        "projects/project_list.html",
        {
            "projects": page_obj,
            "page_obj": page_obj,
            "all_skills": all_skills,
            "active_skill": active_skill,
        },
    )


def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related("owner").prefetch_related("skills", "participants"),
        pk=project_id,
    )
    return render(
        request,
        "projects/project-details.html",
        {"project": project}
    )


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        return redirect("projects:project_detail", project_id=project.id)

    return render(
        request,
        "projects/create-project.html",
        {"form": form, "is_edit": False},
    )


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner_id != request.user.id:
        return HttpResponseForbidden(
            "Редактировать проект может только владелец."
        )

    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        project = form.save()
        return redirect("projects:project_detail", project_id=project.id)

    return render(
        request,
        "projects/create-project.html",
        {"form": form, "is_edit": True, "project": project},
    )


@login_required
@require_POST
def complete_project(request, project_id):
    project, error_response = _get_project_for_json(project_id)
    if error_response:
        return error_response

    if project.owner_id != request.user.id:
        return json_error("forbidden", HTTPStatus.FORBIDDEN)

    project.status = Project.STATUS_CLOSED
    project.save(update_fields=["status", "updated_at"])
    return JsonResponse({"status": "ok"})


@login_required
@require_POST
def toggle_participate(request, project_id):
    project, error_response = _get_project_for_json(project_id)
    if error_response:
        return error_response

    if project.owner_id == request.user.id:
        return json_error("owner_cannot_join", HTTPStatus.BAD_REQUEST)

    if project.participants.filter(id=request.user.id).exists():
        project.participants.remove(request.user)
        participant = False
    else:
        project.participants.add(request.user)
        participant = True

    return JsonResponse({"status": "ok", "participant": participant})


@require_GET
def skills_autocomplete(request):
    query = request.GET.get("q", "").strip()
    skills = Skill.objects.all()
    if query:
        skills = skills.filter(name__icontains=query)
    data = [
        {"id": skill.id, "name": skill.name}
        for skill in skills.order_by("name")[:SKILL_AUTOCOMPLETE_LIMIT]
    ]
    return JsonResponse(data, safe=False)


@login_required
@require_POST
def add_project_skill(request, project_id):
    project, error_response = _get_project_for_json(project_id)
    if error_response:
        return error_response

    if project.owner_id != request.user.id:
        return json_error("forbidden", HTTPStatus.FORBIDDEN)

    payload = json_payload(request)
    skill = None

    skill_id = payload.get("skill_id")
    if skill_id:
        skill = Skill.objects.filter(pk=skill_id).first()
        if skill is None:
            return json_error("skill_not_found", HTTPStatus.NOT_FOUND)
    else:
        raw_name = str(payload.get("name", "")).strip()
        if not raw_name:
            return json_error("name_required", HTTPStatus.BAD_REQUEST)
        normalized_name = " ".join(raw_name.split())[:SKILL_NAME_MAX_LENGTH]
        skill = Skill.objects.filter(name__iexact=normalized_name).first()
        if skill is None:
            skill = Skill.objects.create(name=normalized_name)

    project.skills.add(skill)
    return JsonResponse({"id": skill.id, "name": skill.name})


@login_required
@require_POST
def remove_project_skill(request, project_id, skill_id):
    project, error_response = _get_project_for_json(project_id)
    if error_response:
        return error_response

    if project.owner_id != request.user.id:
        return json_error("forbidden", HTTPStatus.FORBIDDEN)

    skill = Skill.objects.filter(pk=skill_id).first()
    if skill is None:
        return json_error("skill_not_found", HTTPStatus.NOT_FOUND)

    project.skills.remove(skill)
    return JsonResponse({"status": "ok"})


def _get_project_for_json(project_id):
    project = Project.objects.filter(pk=project_id).first()
    if project is None:
        return None, json_error("project_not_found", HTTPStatus.NOT_FOUND)
    return project, None
