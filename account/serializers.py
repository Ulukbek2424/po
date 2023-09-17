from rest_framework import serializers

from django.conf import settings
from django.db import transaction
from django.contrib.auth.hashers import make_password

from .models import User, Waiter, Admin, Token

class WaiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waiter
        fields = ['email', 'password', 'name', 'lang']

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("password must be longer than 6 characters")
        return value

    def save(self, **kwargs):
        with transaction.atomic():
            user = User.objects.create(is_waiter=True)
            password = self.validated_data['password']
            hashed_password = make_password(password)
            Waiter.objects.create(
                user=user,
                email=self.validated_data['email'],
                password=hashed_password,
                name=self.validated_data['name'],
                lang=self.validated_data['lang']
            )
            token = Token.objects.filter(user=user).first()
            if not token:
                token = Token.objects.create(user=user)

        return token


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['email', 'password', 'name', 'lang']

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("password must be longer than 6 characters")
        return value

    def save(self, **kwargs):
        with transaction.atomic():
            user = User.objects.create(is_admin=True)
            password = self.validated_data['password']
            hashed_password = make_password(password)
            Admin.objects.create(
                user=user,
                email=self.validated_data['email'],
                password=hashed_password,
                name=self.validated_data['name'],
                lang=self.validated_data['lang']
            )
            token = Token.objects.filter(user=user).first()
            if not token:
                token = Token.objects.create(user=user)

        return token
