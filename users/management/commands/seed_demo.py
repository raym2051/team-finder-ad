from django.core.management.base import BaseCommand

from projects.models import Project, Skill
from users.models import User


DEMO_PASSWORD = "review12345"


USERS = [
    {
        "email": "anna@teamfinder.local",
        "name": "Анна",
        "surname": "Морозова",
        "phone": "+7 900 200-10-01",
        "github_url": "https://github.com/anna-morozova",
        "about": "Team Lead и архитектор микросервисов. Люблю Go и Python.",
    },
    {
        "email": "dmitry@teamfinder.local",
        "name": "Дмитрий",
        "surname": "Волков",
        "phone": "+7 900 200-10-02",
        "github_url": "https://github.com/dmitry-volkov",
        "about": "ML Engineer, строю нейросети для задач компьютерного зрения.",
    },
    {
        "email": "elena@teamfinder.local",
        "name": "Елена",
        "surname": "Крылова",
        "phone": "+7 900 200-10-03",
        "github_url": "https://github.com/elena-krylova",
        "about": "DevOps инженер, автоматизирую развертывание и CI/CD.",
    },
    {
        "email": "ivan@teamfinder.local",
        "name": "Иван",
        "surname": "Белов",
        "phone": "+7 900 200-10-04",
        "github_url": "https://github.com/ivan-belov",
        "about": "Fullstack разработчик, пишу на Django и React.",
    },
    {
        "email": "olga@teamfinder.local",
        "name": "Ольга",
        "surname": "Новикова",
        "phone": "+7 900 200-10-05",
        "github_url": "https://github.com/olga-novikova",
        "about": "QA Automation, пишу тесты на Playwright и Pytest.",
    },
]


PROJECTS = [
    {
        "owner": "anna@teamfinder.local",
        "name": "TaskFlow",
        "description": (
            "Система управления задачами с канами, спринтами и аналитикой времени. "
            "Аналог Trello для маленьких команд."
        ),
        "github_url": "https://github.com/example/taskflow",
        "skills": ["Django", "Django REST", "PostgreSQL", "Redis", "Celery"],
    },
    {
        "owner": "dmitry@teamfinder.local",
        "name": "FaceRecog",
        "description": (
            "Сервис распознавания лиц на фотографиях. Использует OpenCV и предобученные "
            "нейросети. Результат возвращает JSON с вероятностью."
        ),
        "github_url": "https://github.com/example/face-recog",
        "skills": ["Python", "OpenCV", "TensorFlow", "FastAPI"],
    },
    {
        "owner": "elena@teamfinder.local",
        "name": "DeployBot",
        "description": (
            "Telegram-бот для автоматического деплоя приложений. Поддерживает GitHub webhooks, "
            "логирование и уведомления о статусе сборки."
        ),
        "github_url": "https://github.com/example/deploy-bot",
        "skills": ["Python", "Docker", "GitHub API", "Telegram Bot API"],
    },
    {
        "owner": "ivan@teamfinder.local",
        "name": "EventHub",
        "description": (
            "Платформа для поиска IT-ивентов: конференции, митапы, хакатоны. "
            "Есть фильтрация по городу, темам и датам."
        ),
        "github_url": "https://github.com/example/eventhub",
        "skills": ["Django", "JavaScript", "Leaflet", "PostgreSQL"],
    },
    {
        "owner": "olga@teamfinder.local",
        "name": "TestGen",
        "description": (
            "Генератор тестовых данных для API. Позволяет создавать JSON-шаблоны "
            "и заполнять их случайными данными по заданным правилам."
        ),
        "github_url": "https://github.com/example/testgen",
        "skills": ["Python", "Pydantic", "Faker", "FastAPI"],
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
