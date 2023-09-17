from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.conf import settings

from .models import Waiter, Admin, Token


class PoAuthBackend(BaseBackend):
    """Класс для авторизации админов/официантов"""

    def authenticate(self, request, type=None, email=None, password=None, lang='ru'):
        token = None

        langs = [language[0] for language in settings.LANGUAGES]
        if lang not in langs:
            lang = 'ru'

        user = None
        if type == 'waiter':
            user = Waiter.objects.filter(email=email).first()
        elif type == 'admin':
            user = Admin.objects.filter(email=email).first()
        if user and check_password(password, user.password):
            if user.lang != lang:
                user.lang = lang
                user.save()
            token = Token.objects.filter(user=user.user).first()
            if not token:
                token = Token.objects.create(user=user.user)

        return token

