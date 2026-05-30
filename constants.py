"""Глобальные константы проекта"""

# Pagination
PAGINATION_PAGE_SIZE = 12

# Skills search
MAX_SKILLS_SEARCH_RESULTS = 10

# Avatar generation
AVATAR_SIZE = 200
AVATAR_FONT_SIZE = 80
AVATAR_BG_COLORS = [
    (255, 204, 204),  # light red
    (204, 255, 204),  # light green
    (204, 204, 255),  # light blue
    (255, 255, 204),  # light yellow
    (255, 204, 255),  # light purple
    (204, 255, 255),  # light cyan
]

# Password validation
MIN_PASSWORD_LENGTH = 8

# Model field max lengths
MAX_NAME_LENGTH = 124
MAX_USERNAME_LENGTH = 150
MAX_EMAIL_LENGTH = 254
MAX_GITHUB_URL_LENGTH = 200
MAX_PROJECT_TITLE_LENGTH = 200
MAX_PROJECT_DESCRIPTION_LENGTH = 1000

# Project statuses
PROJECT_STATUS_OPEN = "open"
PROJECT_STATUS_CLOSED = "closed"
PROJECT_STATUS_ARCHIVED = "archived"

PROJECT_STATUS_CHOICES = [
    (PROJECT_STATUS_OPEN, "Open"),
    (PROJECT_STATUS_CLOSED, "Closed"),
    (PROJECT_STATUS_ARCHIVED, "Archived"),
]
