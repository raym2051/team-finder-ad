"""Вспомогательные функции"""

import hashlib
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from PIL import Image, ImageDraw, ImageFont
from projects.models import Skill

from team_finder.constants import (
    AVATAR_BG_COLORS,
    AVATAR_FONT_SIZE,
    AVATAR_SIZE,
    AVATAR_TEXT_COLOR,
    MAX_SKILLS_SEARCH_RESULTS,
    PAGINATION_PAGE_SIZE,
)


def generate_avatar(name):
    """
    Генерирует аватарку на основе имени пользователя.
    Только при создании пользователя, если у него нет загруженного аватара или смене именни
    """

    if not name:
        name = "User"

    parts = name.strip().split()
    if parts:
        first_letter = parts[0][0].upper()
    else:
        first_letter = "U"

    # Определяем цвет фона на основе хеша имени
    hash_object = hashlib.md5(name.encode())
    color_index = int(hash_object.hexdigest(), 16) % len(AVATAR_BG_COLORS)
    bg_color = AVATAR_BG_COLORS[color_index]

    image = Image.new("RGB", (AVATAR_SIZE, AVATAR_SIZE), bg_color)
    draw = ImageDraw.Draw(image)

    # Пытаемся загрузить шрифт побольше
    font = None
    for font_path in [
        "/System/Library/Fonts/Helvetica.ttc",  # macOS
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
        "arial.ttf",  # Windows
    ]:
        try:
            font = ImageFont.truetype(font_path, AVATAR_FONT_SIZE)
            break
        except (OSError, IOError):
            continue

    # Рисуем букву
    if font is None:
        # Дефолтный шрифт
        font = ImageFont.load_default()
        x = AVATAR_SIZE // 3
        y = AVATAR_SIZE // 3
    else:
        # Центрируем для нормального шрифта
        bbox = draw.textbbox((0, 0), first_letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (AVATAR_SIZE - text_width) // 2
        y = (AVATAR_SIZE - text_height) // 2

    draw.text((x, y), first_letter, fill=AVATAR_TEXT_COLOR, font=font)

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    safe_name = name.replace(" ", "_").replace("/", "_")
    return ContentFile(buffer.read(), name=f"avatar_{safe_name}.png")


def paginate_queryset(request, queryset, page_size=PAGINATION_PAGE_SIZE):
    """
    Универсальная функция для пагинации
    Возвращает page_obj
    """
    paginator = Paginator(queryset, page_size)
    page_number = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return page_obj


def get_skills_autocomplete(query):
    """
    Поиск навыков для автокомплита
    """
    if not query:
        return []

    return list(Skill.objects.filter(name__istartswith=query).order_by("name")[:MAX_SKILLS_SEARCH_RESULTS])
