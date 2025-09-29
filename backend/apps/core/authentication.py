from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()

class MixedAuthentication(BaseAuthentication):
    """
    Підтримує JWT (Authorization: Bearer <token>) та legacy token (X-Employee-Token).
    JWT має пріоритет, якщо в заголовках є Authorization.
    """
    def authenticate(self, request):
        auth = JWTAuthentication()
        header = request.headers.get('Authorization')
        if header:
            # делегуємо JWT auth
            try:
                user_auth_tuple = auth.authenticate(request)
                if user_auth_tuple:
                    return user_auth_tuple
            except Exception:
                pass  # якщо JWT не валідний, далі перевіримо legacy

        legacy = request.headers.get('X-Employee-Token')
        if legacy:
            try:
                user = User.objects.get(legacy_token=legacy)
                return (user, None)
            except User.DoesNotExist:
                return None
        return None
