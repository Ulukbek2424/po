from django.utils import timezone

from account.models import User, Waiter, Admin

from .user_change_lang_service import UserChangeLangService, create_flags


class UserAuthService:
    """Сервис по авторизации пользователей"""

    def __init__(self, email, password, name, lang):
        self.email = email
        self.password = password
        self.name = name
        self.lang = lang


    def execute_waiter(self):
        try:
            # Пытаемся получить официанта
            waiter = Waiter.objects.get(email=self.email)
        except Waiter.DoesNotExist:
            # Создаем нового официанта
            waiter = Waiter(email=self.email, password=self.password, name=self.name, lang=self.lang)
            waiter.save()
        return waiter


    def execute_admin(self):
        try:
            # Пытаемся получить админа
            admin = Admin.objects.get(email=self.email)
        except Admin.DoesNotExist:
            # Создаем нового админа
            admin = Admin(email=self.email, password=self.password, name=self.name, lang=self.lang)
            admin.save()
        return admin
