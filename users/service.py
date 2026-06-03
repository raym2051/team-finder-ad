"""Вспомогательные функции"""

import hashlib
from io import BytesIO

from constants import (
    AVATAR_BG_COLORS,
    AVATAR_FONT_SIZE,
    AVATAR_SIZE,
    MAX_SKILLS_SEARCH_RESULTS,
)
from django.users.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from projects.models import Skill


def generate_avatar(name):
    """
    Генерирует аватарку на основе имени пользователя
    """
    # Определяем цвет фона на основе хеша имени
    hash_object = hashlib.md5(name.encode())
    color_index = int(hash_object.hexdigest(), 16) % len(AVATAR_BG_COLORS)
    bg_color = AVATAR_BG_COLORS[color_index]

    # Создаем изображение
    image = Image.new("RGB", (AVATAR_SIZE, AVATAR_SIZE), bg_color)
    draw = ImageDraw.Draw(image)

    # Берем первую букву и переводим в верхний регистр
    first_letter = name[0].upper() if name else "?"

    # Пытаемся загрузить шрифт побольше, если нет - используем дефолтный
    try:
        # Для Linux/Mac
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", AVATAR_FONT_SIZE
        )
    except (OSError, IOError):  # Исправлено: конкретные исключения вместо bare except
        try:
            # Для Windows
            font = ImageFont.truetype("arial.ttf", AVATAR_FONT_SIZE)
        except (OSError, IOError):  # Исправлено: конкретные исключения
            # Дефолтный шрифт
            font = ImageFont.load_default()

    # Рассчитываем позицию для центрирования текста
    bbox = draw.textbbox((0, 0), first_letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (AVATAR_SIZE - text_width) // 2
    y = (AVATAR_SIZE - text_height) // 2

    # Рисуем текст белым цветом
    draw.text((x, y), first_letter, fill=(255, 255, 255), font=font)

    # Сохраняем в BytesIO
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return ContentFile(buffer.read(), name=f"avatar_{name}.png")


def paginate_queryset(request, queryset, page_size):
    """
    Универсальная функция для пагинации
    Возвращает (paginator, page_obj)
    """
    from django.users.paginator import EmptyPage, PageNotAnInteger, Paginator

    paginator = Paginator(queryset, page_size)
    page_number = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return paginator, page_obj


def get_skills_autocomplete(query):
    """
    Поиск навыков для автокомплита
    """
    if not query:
        return []

    return list(
        Skill.objects.filter(name__istartswith=query).order_by("name")[
            :MAX_SKILLS_SEARCH_RESULTS
        ]
    )
