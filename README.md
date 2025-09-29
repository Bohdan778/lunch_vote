Lunch Vote — тестове завдання
Що це

Це простий сервіс, де співробітники можуть голосувати за меню ресторану на сьогодні.

Технології, які я використав:

Django + DRF

JWT через djangorestframework-simplejwt

PostgreSQL

Docker + docker-compose

PyTest для тестів

Як запустити локально (через Docker)

Створіть файл .env з мінімумом:

SECRET_KEY=your_secret_here
DEBUG=1


Запустіть Docker:

docker-compose up --build


Сайт буде доступний на http://localhost:8000/

Міграції

В docker-compose у мене налаштовано, щоб міграції йшли автоматично.
Якщо треба вручну:

docker-compose exec web python manage.py migrate

API

POST /api/auth/token/ — отримати JWT токен (логін/пароль)

POST /api/employees/ — створити співробітника (повертає legacy token)

POST /api/restaurants/ — створити ресторан (треба бути авторизованим)

POST /api/restaurants/{id}/menus/ — завантажити меню на день

GET /api/menus/today/?restaurant={id} — подивитися меню на сьогодні

POST /api/menus/{menu_id}/vote/ — проголосувати (JWT або X-Employee-Token)

GET /api/results/today/?restaurant={id} — результати за сьогодні

Тести

Щоб прогнати тести локально:

docker-compose exec web pytest -q

Лінтер

Використав flake8 для перевірки коду.
Запускати так:

docker-compose exec web flake8

Підтримка старих і нових клієнтів

Нові клієнти працюють через Authorization: Bearer <jwt>

Старі клієнти через X-Employee-Token (legacy token)

Все працює в одній в’юшці через кастомну MixedAuthentication

Що я намагався робити по SOLID і чистому коду

Логіку розділяв на models, serializers, views, services (щоб не робити дуже великі в’юшки)

Використовував DRF generics / viewsets

Писав тести на головні сценарії: голосування, завантаження меню, edge cases

Старався писати зрозумілі назви змінних, type hints там, де логіка трохи складна

Перевіряв код через flake8

Що можу зробити далі

Можу згенерувати повні файли проекту (models.py, views.py, serializers.py, settings.py з env, manage.py і т.д.)

Можу додати тести на граничні випадки

Можу допомогти налаштувати Docker Compose і .env

Можу додати flake8 і pre-commit конфігурації
