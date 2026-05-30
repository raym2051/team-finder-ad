"""Админ-панель для проектов и навыков"""

from django.contrib import admin

from projects.models import Project, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Админ-панель навыков"""

    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Админ-панель проектов"""

    list_display = ("title", "author", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "author__username")
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("participants", "skills")
