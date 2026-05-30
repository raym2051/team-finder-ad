from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path("list/", views.project_list, name="project_list"),
    path("create-project/", views.create_project_view, name="create_project"),
    path("<int:project_id>/", views.project_detail_view, name="project_detail"),
    path("<int:project_id>/edit/", views.edit_project_view, name="edit_project"),
    path("<int:project_id>/join/", views.join_project_view, name="join_project"),
    path(
        "<int:project_id>/complete/",
        views.complete_project_view,
        name="complete_project",
    ),
    path("skills/", views.skill_autocomplete_view, name="skill_autocomplete"),
    path("<int:project_id>/skills/add/", views.add_skill_view, name="add_skill"),
    path(
        "<int:project_id>/skills/<int:skill_id>/remove/",
        views.remove_skill_view,
        name="remove_skill",
    ),
]
