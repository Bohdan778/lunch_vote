from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Розширюємо стандартного користувача, додаючи legacy token
class Employee(AbstractUser):
    legacy_token = models.CharField(max_length=64, blank=True, null=True, unique=True)
    # можна додати поле role/department тощо

def generate_legacy_token():
    import secrets
    return secrets.token_hex(32)

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='menus', on_delete=models.CASCADE)
    date = models.DateField()
    # зберігаємо структуру меню як JSON: list of items {name, price, desc}
    items = models.JSONField(default=list)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('restaurant', 'date')

    def __str__(self):
        return f"{self.restaurant.name} - {self.date.isoformat()}"

class Vote(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='votes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'menu')
