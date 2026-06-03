# TeamFinder

TeamFinder — учебное Django-приложение для поиска участников в проекты. Реализован вариант 3: необходимые навыки проекта, автодополнение навыков, создание новых навыков и фильтрация списка проектов по `?skill=<Название>`.

## Что уже есть

- PostgreSQL используется как основная база данных.
- Docker Compose поднимает базу и web-приложение.
- Данные PostgreSQL и загруженные медиа сохраняются в Docker volumes.
- Есть несколько демо-пользователей, у каждого создан минимум один проект.
- Главная страница, список проектов и alias `/project/list/` ведут на список проектов.
- Реализованы регистрация, вход по email, выход, профили, редактирование профиля, смена пароля, список участников, CRUD проектов, участие в проектах и завершение проекта владельцем.
- На странице проекта владелец может добавлять, создавать и удалять навыки без перезагрузки страницы.
- На странице `/projects/list/` работает фильтр по навыку, активный фильтр подсвечивается, есть сброс.

## Быстрый запуск через Docker Compose

```bash
docker compose up --build
```

После запуска:

- сайт: [http://localhost:8000](http://localhost:8000)
- админка: [http://localhost:8000/admin/](http://localhost:8000/admin/)

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

Пароль для всех демо-пользователей:

```text
review12345
```

Пользователи:

- `test1@example.com`
- `test2@example.com`
- `test3@example.com`
- `test4@example.com`

## Локальный запуск без Docker web-контейнера

1. Создайте окружение и установите зависимости:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Скопируйте переменные окружения:

```bash
cp .env_example .env
```

3. Поднимите только PostgreSQL:

```bash
docker compose up -d db
```

4. Примените миграции и создайте демо-данные:

```bash
python manage.py migrate
python manage.py seed_demo
```

5. Запустите сервер:

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

1. Войдите под `alisa@teamfinder.local` / `review12345`.
2. Откройте любой проект Алисы, например `StudyFlow`.
3. В блоке «Необходимые навыки» нажмите «+ Добавить навык».
4. Начните вводить навык: существующие навыки появятся в автодополнении, нового навыка можно создать нажатием Enter.
5. Удалите навык крестиком: изменение происходит без перезагрузки.
6. Перейдите на `/projects/list/` и нажмите на чип навыка или откройте `/projects/list/?skill=Django`.
7. В списке останутся только проекты с выбранным навыком; активный фильтр подсвечен, рядом есть сброс.
