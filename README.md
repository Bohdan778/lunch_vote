# Lunch Vote — тестове завдання

## Опис проекту
Це простий сервіс, де співробітники можуть голосувати за меню ресторану на сьогодні.  
Мета була — показати базову роботу з Django, DRF, JWT та Docker, а також написати тести.

**Технології:**
- Django + Django REST Framework (DRF)
- JWT (через `djangorestframework-simplejwt`)
- PostgreSQL
- Docker + docker-compose
- PyTest для тестів

---

## Запуск проекту локально (через Docker)

1. Створіть файл `.env` з мінімумом:

SECRET_KEY=your_secret_here
DEBUG=1


2. Запустіть контейнер:

bash docker-compose up --build

3. Сайт буде доступний на:

http://localhost:8000/


5. Сайт буде доступний на:

Міграції

У docker-compose налаштовано, щоб міграції йшли автоматично.
Якщо потрібно запустити вручну:
docker-compose exec web python manage.py migrate

API
Метод	URL	Опис
POST	/api/auth/token/	Отримати JWT токен (username, password)
POST	/api/employees/	Створити співробітника (повертає legacy token)
POST	/api/restaurants/	Створити ресторан (потрібна автентифікація)
POST	/api/restaurants/{id}/menus/	Завантажити меню на день
GET	/api/menus/today/?restaurant={id}	Отримати меню на сьогодні
POST	/api/menus/{menu_id}/vote/	Проголосувати (JWT або X-Employee-Token)
GET	/api/results/today/?restaurant={id}	Отримати результати за сьогодні

Тести

Щоб прогнати тести локально:

docker-compose exec web pytest -q


Лінтер

Використав flake8 для перевірки коду.
Запуск:

docker-compose exec web flake8


Підтримка старих і нових клієнтів

Нові клієнти працюють через Authorization: Bearer <jwt>

Старі клієнти через X-Employee-Token (legacy token)

Для цього зроблена кастомна MixedAuthentication, яка перевіряє JWT, а потім legacy token.

Що я робив для якості коду

Логіку розділив на модулі: models, serializers, views, services

Використовував DRF generics / viewsets, щоб не робити великі в’юшки

Писав тести для основних сценаріїв і edge cases

Старався писати зрозумілі назви змінних і type hints

Перевіряв код через flake8

Можливі кроки далі

Згенерувати повні файли проекту (models.py, views.py, serializers.py, settings.py, manage.py)

Додати тести на граничні випадки

Налаштувати Docker Compose і .env

Додати flake8 та pre-commit для перевірки і форматування коду

