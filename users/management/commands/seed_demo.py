from django.core.management.base import BaseCommand

from projects.models import Project, Skill
from users.models import User

DEMO_PASSWORD = "review12345"

USERS = [
    {
        "email": "test1@example.com",
        "name": "Алексей",
        "surname": "Иванов",
        "phone": "+7 900 111-11-11",
        "github_url": "https://github.com/test1",
        "about": "Backend-разработчик на Django и FastAPI.",
    },
    {
        "email": "test2@example.com",
        "name": "Мария",
        "surname": "Петрова",
        "phone": "+7 900 222-22-22",
        "github_url": "https://github.com/test2",
        "about": "Frontend-разработчик, React и Vue.js.",
    },
    {
        "email": "test3@example.com",
        "name": "Игорь",
        "surname": "Сидоров",
        "phone": "+7 900 333-33-33",
        "github_url": "https://github.com/test3",
        "about": "Data Scientist, Python и машинное обучение.",
    },
    {
        "email": "test4@example.com",
        "name": "Екатерина",
        "surname": "Кузнецова",
        "phone": "+7 900 444-44-44",
        "github_url": "https://github.com/test4",
        "about": "DevOps инженер, Docker и CI/CD.",
    },
]

PROJECTS = [{"owner": "test1@example.com",
             "name": "TaskMaster",
             "description": "Умный планировщик задач с интеграцией Telegram-бота и аналитикой времени.",
             "github_url": "https://github.com/test1/taskmaster",
             "skills": ["Django",
                        "PostgreSQL",
                        "Redis",
                        "Celery"],
             },
            {"owner": "test2@example.com",
             "name": "EventHub",
             "description": "Платформа для поиска IT-мероприятий и нетворкинга с картой и фильтрами.",
             "github_url": "https://github.com/test2/eventhub",
             "skills": ["React",
                        "Django REST",
                        "Leaflet"],
             },
            {"owner": "test3@example.com",
             "name": "DataViz",
             "description": "Веб-инструмент для визуализации датасетов: загрузка CSV, графики, экспорт.",
             "github_url": "https://github.com/test3/dataviz",
             "skills": ["Python",
                        "Pandas",
                        "Plotly",
                        "Django"],
             },
            {"owner": "test4@example.com",
             "name": "DeployFlow",
             "description": "Автоматизация деплоя через GitHub Actions: линтеры, тесты, уведомления.",
             "github_url": "https://github.com/test4/deployflow",
             "skills": ["Python",
                        "Docker",
                        "GitHub Actions",
                        "FastAPI"],
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
