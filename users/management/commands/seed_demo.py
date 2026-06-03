from django.core.management.base import BaseCommand

from projects.models import Project, Skill
from users.models import User


DEMO_PASSWORD = "review12345"


USERS = [
    {
        "email": "alisa@teamfinder.local",
        "name": "Алиса",
        "surname": "Соколова",
        "phone": "+7 900 100-10-01",
        "github_url": "https://github.com/alisa-sokolova",
        "about": "Backend-разработчица, любит аккуратные API и понятные README.",
    },
    {
        "email": "timur@teamfinder.local",
        "name": "Тимур",
        "surname": "Валеев",
        "phone": "+7 900 100-10-02",
        "github_url": "https://github.com/timur-valeev",
        "about": "Frontend-инженер, собирает интерфейсы для учебных и pet-проектов.",
    },
    {
        "email": "mira@teamfinder.local",
        "name": "Мира",
        "surname": "Орлова",
        "phone": "+7 900 100-10-03",
        "github_url": "https://github.com/mira-orlova",
        "about": "Product-minded дизайнер, помогает превращать идеи в понятные сценарии.",
    },
    {
        "email": "gleb@teamfinder.local",
        "name": "Глеб",
        "surname": "Никитин",
        "phone": "+7 900 100-10-04",
        "github_url": "https://github.com/gleb-nikitin",
        "about": "Python-разработчик, интересуется автоматизацией, тестами и данными.",
    },
]


PROJECTS = [
    {
        "owner": "alisa@teamfinder.local",
        "name": "StudyFlow",
        "description": (
            "Планировщик учебных спринтов для небольших команд: задачи, дедлайны, "
            "еженедельные итоги и прозрачное распределение ответственности."
        ),
        "github_url": "https://github.com/example/studyflow",
        "skills": ["Django", "PostgreSQL", "REST API"],
    },
    {
        "owner": "timur@teamfinder.local",
        "name": "Campus Market",
        "description": (
            "Мини-маркетплейс для студенческих вещей и услуг с личными профилями, "
            "избранным и быстрыми карточками объявлений."
        ),
        "github_url": "https://github.com/example/campus-market",
        "skills": ["React", "JavaScript", "UI"],
    },
    {
        "owner": "mira@teamfinder.local",
        "name": "Pitch Room",
        "description": (
            "Пространство для подготовки презентаций проектов: структура питча, "
            "комментарии участников и чек-листы перед демо-днём."
        ),
        "github_url": "https://github.com/example/pitch-room",
        "skills": ["UX", "Copywriting", "Research"],
    },
    {
        "owner": "gleb@teamfinder.local",
        "name": "Data Garden",
        "description": (
            "Небольшой сервис для визуализации учебной статистики: загрузка CSV, "
            "графики прогресса и экспорт отчётов."
        ),
        "github_url": "https://github.com/example/data-garden",
        "skills": ["Python", "Pandas", "Charts"],
    },
]


class Command(BaseCommand):
    help = "Creates demo TeamFinder users, projects, and skills for reviewers."

    def handle(self, *args, **options):
        users_by_email = {}
        for user_data in USERS:
            user, created = User.objects.get_or_create(
                email=user_data["email"],
                defaults={
                    "name": user_data["name"],
                    "surname": user_data["surname"],
                    "phone": user_data["phone"],
                    "github_url": user_data["github_url"],
                    "about": user_data["about"],
                },
            )
            if created:
                user.set_password(DEMO_PASSWORD)
                user.save(update_fields=["password"])
            users_by_email[user.email] = user

        for project_data in PROJECTS:
            owner = users_by_email[project_data["owner"]]
            project, _ = Project.objects.get_or_create(
                owner=owner,
                name=project_data["name"],
                defaults={
                    "description": project_data["description"],
                    "github_url": project_data["github_url"],
                },
            )
            for skill_name in project_data["skills"]:
                skill, _ = Skill.objects.get_or_create(name=skill_name)
                project.skills.add(skill)

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo data is ready. Password for demo users: {DEMO_PASSWORD}"
            )
        )
