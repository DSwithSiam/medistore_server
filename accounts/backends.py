from django.contrib.auth.backends import BaseBackend
from .models import User


class EmailBackend(BaseBackend):
    """
    Custom authentication backend that authenticates users using email instead of username.
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get("username")  # Fallback for Django's default behavior

        if email is None or password is None:
            return None

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        return user if user.check_password(password) and user.is_active else None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
