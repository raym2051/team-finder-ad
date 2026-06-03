import json

from django.http import JsonResponse


def json_payload(request):
    """Извлекает JSON-данные из тела запроса."""
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return {}


def json_error(error, status):
    """Возвращает стандартный JSON-ответ с ошибкой."""
    return JsonResponse({"status": "error", "error": error}, status=status)
