from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class HardcodedAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username == 'ingenieriaweb' and password == 'ucse':
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Crear el usuario si no existe
                user = User(username=username)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        return None
