import traceback
from django.contrib import auth

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, BasePermission

from .models import Token
from .serializers import WaiterSerializer, AdminSerializer
from .exceptions import TokenDoesNotExist


class WaiterRegistrationView(APIView):
    serializer_class = WaiterSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            token = serializer.save()
            if not token:
                raise TokenDoesNotExist("cannot register user")
            result = {'success': 1, 'token': token.key}
            return Response(result)
        except serializers.ValidationError as e:
            errors = dict(e.detail)
            errors['success'] = 0
            return Response(errors)
        except TokenDoesNotExist as e:
            return Response({'success': 0, 'user': [str(e)]})


class AdminRegistrationView(APIView):
    serializer_class = AdminSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            token = serializer.save()
            if not token:
                raise TokenDoesNotExist("cannot register user")
            result = {'success': 1, 'token': token.key}
            return Response(result)
        except serializers.ValidationError as e:
            errors = dict(e.detail)
            errors['success'] = 0
            return Response(errors)
        except TokenDoesNotExist as e:
            return Response({'success': 0, 'user': [str(e)]})


class WaiterLoginView(APIView):

    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            lang = request.data.get('lang', 'ru')

            token = auth.authenticate(request, type='waiter', email=email, password=password, lang=lang)

            if not token:
                raise TokenDoesNotExist("email or password is invalid")
            result = {'success': 1, 'token': token.key}
            return Response(result)
        except TokenDoesNotExist as e:
            return Response({'success': 0, 'user': [str(e)]})
        except Exception as e:
            return Response({'success': 0, 'error': [str(e)]})


class AdminLoginView(APIView):

    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            lang = request.data.get('lang', 'ru')

            token = auth.authenticate(request, type='admin', email=email, password=password, lang=lang)

            if not token:
                raise TokenDoesNotExist("email or password is invalid")
            result = {'success': 1, 'token': token.key}
            return Response(result)
        except TokenDoesNotExist as e:
            return Response({'success': 0, 'user': [str(e)]})
        except Exception as e:
            return Response({'success': 0, 'error': [str(e)]})


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            Token.objects.filter(user=request.user).delete()
            return Response({'success': 1})
        except Exception as e:
            return Response({'success': 0, 'error': [str(e)]})


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_admin

class IsWaiter(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_waiter
