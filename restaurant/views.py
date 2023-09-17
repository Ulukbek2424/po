import traceback
from django.contrib import auth

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, BasePermission

from account.views import IsAdmin, IsWaiter

from .models import Restaurant, Branch, MenuCategory, Product
from .serializers import RestaurantSerializer, BranchSerializer, MenuCategorySerializer, ProductSerializer
from .exceptions import ProductAndMenuCategoryDoesNotMatch


class IsRestaurantAdmin(BasePermission):
    def has_permission(self, request, view):
        restaurant_id = view.kwargs.get('restaurant_id')
        restaurant = Restaurant.objects.filter(pk=restaurant_id).first()
        return restaurant and restaurant.admin == request.user.admin

class IsBranchAdmin(BasePermission):
    def has_permission(self, request, view):
        branch_id = view.kwargs.get('branch_id')
        branch = Branch.objects.filter(pk=branch_id).first()
        return branch and branch.restaurant and branch.restaurant.admin == request.user.admin

class IsMenuCategoryAdmin(BasePermission):
    def has_permission(self, request, view):
        menu_category_id = view.kwargs.get('menu_category_id')
        menu_category = MenuCategory.objects.filter(pk=menu_category_id).first()
        return menu_category and menu_category.restaurant and menu_category.restaurant.admin == request.user.admin


class IsProductAdmin(BasePermission):
    def has_permission(self, request, view):
        product_id = view.kwargs.get('product_id')
        product = Product.objects.filter(pk=product_id).first()
        return product and product.menu_category and product.menu_category.restaurant \
                       and product.menu_category.restaurant.admin == request.user.admin



class RestaurantCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = RestaurantSerializer

    def post(self, request):
        try:
            admin = request.user.admin
            data = {"admin": admin}
            if "icon" in request.data:
                data.update(icon=request.data.get("icon"))
            if "photos" in request.data:
                data.update(photos=request.data.get("photos"))
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            restaurant_id = serializer.save(**data)
            result = {'success': 1, 'restaurant_id': restaurant_id}
            return Response(result)
        except serializers.ValidationError as e:
            errors = dict(e.detail)
            errors['success'] = 0
            return Response(errors)
        except Exception as e:
            return Response({'success': 0, 'error': [str(e)]})


class RestaurantUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin, IsRestaurantAdmin]
    serializer_class = RestaurantSerializer

    def put(self, request, restaurant_id):
        try:
            admin = request.user.admin
            data = {"admin": admin}
            if "icon" in request.data:
                data.update(icon=request.data.get("icon"))
            if "photos" in request.data:
                data.update(photos=request.data.get("photos"))
            restaurant = Restaurant.objects.get(pk=restaurant_id)
            serializer = self.serializer_class(restaurant, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.update(restaurant, serializer.validated_data, **data)
            result = {'success': 1}
            return Response(result)
        except Restaurant.DoesNotExist:
            return Response({'success': 0, 'restaurant': ['Restaurant not found']})
        except serializers.ValidationError as e:
            errors = dict(e.detail)
            errors['success'] = 0
            return Response(errors)
        except Exception as e:
            return Response({'success': 0, 'error': str(e)})

    def delete(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
            restaurant.delete()
            return Response({'success': 1})
        except Restaurant.DoesNotExist:
            return Response({'success': 0, 'restaurant': ['Restaurant not found']})
        except Exception as e:
            return Response({'success': 0, 'error': str(e)})


class BranchCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin, IsRestaurantAdmin]
    serializer_class = BranchSerializer

    def post(self, request, restaurant_id):
        try:
            data = {"restaurant": restaurant_id, "address": request.data.get("address")}
            if "photos" in request.data:
                data.update(photos=request.data.get("photos"))
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            branch_id = serializer.save(**data)
            result = {'success': 1, 'branch_id': branch_id}
            return Response(result)
        except serializers.ValidationError as e:
            errors = dict(e.detail)
            errors['success'] = 0
            return Response(errors)
        except Exception as e:
            print(traceback.format_exc())
            return Response({'success': 0, 'error': [str(e)]})


class BranchUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin, IsBranchAdmin]
    serializer_class = BranchSerializer

    def put(self, request, branch_id):
        try:
            branch = Branch.objects.get(pk=branch_id)
            data = {"address": request.data.get("address")}
            if "photos" in request.data:
                data.update(photos=request.data.get("photos"))
            serializer = self.serializer_class(branch, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.update(branch, **data)
            result = {'success': 1}
            return Response(result)
        except Branch.DoesNotExist:
            return Response({'success': 0, 'branch': ['Branch not found']})
        except Exception as e:
            return Response({'success': 0, 'error': str(e)})

    def delete(self, request, branch_id):
        try:
            branch = Branch.objects.get(pk=branch_id)
            branch.delete()
            return Response({'success': 1})
        except Branch.DoesNotExist:
            return Response({'success': 0, 'branch': ['Branch not found']})
        except Exception as e:
            print(traceback.format_exc())
            return Response({'success': 0, 'error': str(e)})


class MenuCategoryCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin, IsRestaurantAdmin]
    serializer_class = MenuCategorySerializer

    def post(self, request, restaurant_id):
        try:
            data = {"restaurant": restaurant_id, "title": request.data.get("title")}
            if "photo" in request.data:
                data.update(photo=request.data.get("photo"))
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            menu_category_id = serializer.save(**data)
            result = {'success': 1, 'menu_category_id': menu_category_id}
            return Response(result)
        except serializers.ValidationError as e:
            errors = dict(e.detail)
            errors['success'] = 0
            return Response(errors)
        except Exception as e:
            print(traceback.format_exc())
            return Response({'success': 0, 'error': [str(e)]})


class MenuCategoryUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin, IsMenuCategoryAdmin]
    serializer_class = MenuCategorySerializer

    def put(self, request, menu_category_id):
        try:
            menu_category = MenuCategory.objects.get(pk=menu_category_id)
            data = {"title": request.data.get("title")}
            if "photo" in request.data:
                data.update(photo=request.data.get("photo"))
            serializer = self.serializer_class(menu_category, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.update(menu_category, **data)
            result = {'success': 1}
            return Response(result)
        except MenuCategory.DoesNotExist:
            return Response({'success': 0, 'menu_category': ['MenuCategory not found']})
        except Exception as e:
            return Response({'success': 0, 'error': str(e)})

    def delete(self, request, menu_category_id):
        try:
            menu_category = MenuCategory.objects.get(pk=menu_category_id)
            menu_category.delete()
            return Response({'success': 1})
        except MenuCategory.DoesNotExist:
            return Response({'success': 0, 'menu_category': ['MenuCategory not found']})
        except Exception as e:
            print(traceback.format_exc())
            return Response({'success': 0, 'error': str(e)})


class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin, IsMenuCategoryAdmin]
    serializer_class = ProductSerializer

    def post(self, request, menu_category_id):
        try:
            data = {"menu_category": menu_category_id, "title": request.data.get("title"),
                    "bottom_price": request.data.get("bottom_price"), "top_price": request.data.get("top_price"),
                    "description": request.data.get("description")}
            if "photo" in request.data:
                data.update(photo=request.data.get("photo"))
            if "branch_ids" in request.data:
                data.update(branch_ids=request.data.get("branch_ids"))
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            product_id = serializer.save(**data)
            result = {'success': 1, 'product_id': product_id}
            return Response(result)
        except serializers.ValidationError as e:
            errors = dict(e.detail)
            errors['success'] = 0
            return Response(errors)
        except Exception as e:
            print(traceback.format_exc())
            return Response({'success': 0, 'error': [str(e)]})


class ProductUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin, IsProductAdmin]
    serializer_class = ProductSerializer

    def put(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            if request.data.get("menu_category_id"):
                menu_category = MenuCategory.objects.get(pk=request.data.get("menu_category_id"))
                if product.menu_category.restaurant != menu_category.restaurant:
                    raise ProductAndMenuCategoryDoesNotMatch("product and menu_category must be from 1 restaurant")
            data = {"menu_category_id": request.data.get("menu_category_id"), "title": request.data.get("title"),
                    "bottom_price": request.data.get("bottom_price"), "top_price": request.data.get("top_price"),
                    "description": request.data.get("description")}
            if "photo" in request.data:
                data.update(photo=request.data.get("photo"))
            if "branch_ids" in request.data:
                data.update(branch_ids=request.data.get("branch_ids"))
            serializer = self.serializer_class(product, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.update(product, **data)
            result = {'success': 1}
            return Response(result)
        except MenuCategory.DoesNotExist:
            return Response({'success': 0, 'menu_category': ['MenuCategory not found']})
        except Product.DoesNotExist:
            return Response({'success': 0, 'product': ['Product not found']})
        except ProductAndMenuCategoryDoesNotMatch as e:
            return Response({'success': 0, 'product': [str(e)]})
        except Exception as e:
            return Response({'success': 0, 'error': str(e)})

    def delete(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            product.delete()
            return Response({'success': 1})
        except Product.DoesNotExist:
            return Response({'success': 0, 'product': ['Product not found']})
        except Exception as e:
            print(traceback.format_exc())
            return Response({'success': 0, 'error': str(e)})
