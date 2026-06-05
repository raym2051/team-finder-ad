# TeamFinder

TeamFinder — учебное Django-приложение для поиска участников в проекты. Реализован вариант 3: необходимые навыки проекта, автодополнение навыков, создание новых навыков и фильтрация списка проектов по `?skill=<Название>`.

## Что уже есть

* PostgreSQL используется как основная база данных.
* Docker Compose поднимает базу и web-приложение.
* Данные PostgreSQL и загруженные медиа сохраняются в Docker volumes.
* Есть несколько демо-пользователей, у каждого создан минимум один проект.
* Главная страница, список проектов и alias `/project/list/` ведут на список проектов.
* Реализованы регистрация, вход по email, выход, профили, редактирование профиля, смена пароля, список участников, CRUD проектов, участие в проектах и завершение проекта владельцем.
* На странице проекта владелец может добавлять, создавать и удалять навыки без перезагрузки страницы.
* На странице `/projects/list/` работает фильтр по навыку, активный фильтр подсвечивается, есть сброс.

## Быстрый запуск через Docker Compose

```bash
docker compose up --build
```

После запуска:

* Сайт: http://localhost:8000
* Админка: http://localhost:8000/admin/

Команда web-контейнера автоматически выполняет:

```bash
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 0.0.0.0:8000
```

Для остановки:

```bash
docker compose down
```

Чтобы удалить сохранённые данные контейнеров:

```bash
docker compose down -v
```

## Демо-аккаунты

Пароль для всех демо-пользователей: `review12345`

Пользователи:

* [test1@example.com](mailto:test1@example.com)
* [test2@example.com](mailto:test2@example.com)
* [test3@example.com](mailto:test3@example.com)
* [test4@example.com](mailto:test4@example.com)

## Локальный запуск без Docker web-контейнера

Создайте окружение и установите зависимости:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Скопируйте переменные окружения:

```bash
cp .env_example .env
```

Поднимите только PostgreSQL:

```bash
docker compose up -d db
```

Примените миграции и создайте демо-данные:

```bash
python manage.py migrate
python manage.py seed_demo
```

Запустите сервер:

```bash
python manage.py runserver
```

## Проверка

Быстрые тесты можно запустить без PostgreSQL через SQLite-переключатель:

```bash
TEAMFINDER_USE_SQLITE=1 python3 manage.py test users projects
```

Проверка конфигурации Django:

```bash
TEAMFINDER_USE_SQLITE=1 python3 manage.py check
```

## Подсказка ревьюеру по варианту 3

1. Войдите под `test1@example.com` / `review12345`.
2. Откройте любой проект пользователя, например **TaskMaster**.
3. В блоке «Необходимые навыки» нажмите **«+ Добавить навык»**.
4. Начните вводить навык: существующие навыки появятся в автодополнении, новый навык можно создать нажатием **Enter**.
5. Удалите навык крестиком — изменение происходит без перезагрузки страницы.
6. Перейдите на `/projects/list/` и нажмите на чип навыка или откройте `/projects/list/?skill=Django`.
7. В списке останутся только проекты с выбранным навыком; активный фильтр будет подсвечен, рядом доступна кнопка сброса.

## Автор

**Roman Demcenko** (raym2051)

* GitHub: https://github.com/raym2051
* Email: [inli.raym@yandex.ru](mailto:inli.raym@yandex.ru)

© 2026 TeamFinder. Учебный проект.
