from django.contrib.auth.backends import BaseBackend
from .models import UserRegistration

class CustomUserBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = UserRegistration.objects.get(email=email)
            if user.check_password(password):
                return user
        except UserRegistration.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserRegistration.objects.get(pk=user_id)
        except UserRegistration.DoesNotExist:
            return None
