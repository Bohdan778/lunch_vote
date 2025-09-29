import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.core.models import Employee, Restaurant, Menu

@pytest.mark.django_db
def test_create_employee_and_use_legacy_token():
    client = APIClient()

    # Створюємо користувача (employee)
    employee_data = {
        "username": "testuser",
        "password": "password123",
        "email": "test@example.com"
    }
    url_create_employee = reverse('core:employee_create')
    response = client.post(url_create_employee, employee_data, format='json')
    assert response.status_code == 201

    # Отримуємо JWT токен
    url_token = reverse('core:token_obtain_pair')
    response = client.post(url_token, {
        "username": employee_data['username'],
        "password": employee_data['password']
    }, format='json')
    assert response.status_code == 200
    access_token = response.data['access']

    # Тестуємо авторизований запит
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    url_today_menus = reverse('core:today_menus')
    response = client.get(url_today_menus)
    assert response.status_code == 200

@pytest.mark.django_db
def test_upload_menu_and_vote():
    client = APIClient()

    # Створюємо restaurant і employee (адміністратора)
    restaurant = Restaurant.objects.create(name="Test Restaurant")
    admin_data = {
        "username": "adminuser",
        "password": "adminpassword",
        "email": "admin@example.com"
    }
    url_create_employee = reverse('core:employee_create')
    response = client.post(url_create_employee, admin_data, format='json')
    assert response.status_code == 201
    employee = Employee.objects.get(username=admin_data['username'])
    employee.is_staff = True  # даємо права адміна
    employee.save()

    # Отримуємо JWT токен
    url_token = reverse('core:token_obtain_pair')
    response = client.post(url_token, {
        "username": admin_data['username'],
        "password": admin_data['password']
    }, format='json')
    assert response.status_code == 200
    access_token = response.data['access']

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    # Завантажуємо меню
    menu_data = {
        "restaurant": restaurant.id,
        "date": "2025-09-29",
        "items": [
            {"name": "Pizza", "price": 10.5},
            {"name": "Salad", "price": 5.0}
        ]
    }
    url_upload_menu = reverse('core:upload_menu', kwargs={"pk": restaurant.id})
    response = client.post(url_upload_menu, menu_data, format='json')
    assert response.status_code == 201

    menu_id = response.data['id']

    # Голосуємо за меню
    url_vote = reverse('core:vote', kwargs={"menu_id": menu_id})
    vote_data = {"employee": employee.id}
    response = client.post(url_vote, vote_data, format='json')
    assert response.status_code == 201
