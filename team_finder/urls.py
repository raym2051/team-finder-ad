from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


def home_redirect(request):
    """Редирект с главной страницы на список проектов"""
    return redirect("projects:project_list")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_redirect, name="home"),
    path("projects/", include("projects.urls")),
    path("users/", include("users.urls", namespace="users")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
