from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

from projects import views as project_views

urlpatterns = [
    path(
        "",
        lambda request: redirect("projects:project_list")),
    path(
        "admin/",
        admin.site.urls),
    path(
        "users/",
        include("users.urls")),
    path(
        "projects/",
        include("projects.urls")),
    path(
        "project/list/",
        project_views.project_list,
        name="legacy_project_list"),
    path(
        "project/list",
        project_views.project_list,
        name="legacy_project_list_no_slash"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
