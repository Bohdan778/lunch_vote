import pytest
from django.utils import timezone
from apps.core.models import Restaurant, Menu, Employee, Vote

@pytest.mark.django_db
def test_menu_unique_per_day():
    r = Restaurant.objects.create(name='R1')
    Menu.objects.create(restaurant=r, date=timezone.localdate(), items=[{"name": "A"}])
    with pytest.raises(Exception):
        # створення ще одного меню для того ж ресторану і дати — має впасти через unique_together
        Menu.objects.create(restaurant=r, date=timezone.localdate(), items=[{"name": "B"}])

@pytest.mark.django_db
def test_vote_uniqueness():
    user = Employee.objects.create_user(username='u', password='p', legacy_token='t')
    r = Restaurant.objects.create(name='R')
    m = Menu.objects.create(restaurant=r, date=timezone.localdate(), items=[])
    Vote.objects.create(employee=user, menu=m)
    with pytest.raises(Exception):
        Vote.objects.create(employee=user, menu=m)
