import os
import string
import random

from rest_framework import serializers

from django.conf import settings
from django.db import transaction

from .models import Restaurant, RestaurantImage, Branch, BranchImage, MenuCategory, Product

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['admin', 'title', 'average_check', 'time_open', 'time_close', 'description']

    def save(self, **kwargs):
        data = dict(self.validated_data, **kwargs)

        with transaction.atomic():
            restaurant = Restaurant.objects.create(
                admin=data["admin"],
                title=data["title"],
                average_check=data["average_check"],
                time_open=data["time_open"],
                time_close=data["time_close"],
                description=data["description"]
            )

            if data.get("icon"):
                dir_path = os.path.join(settings.BASE_DIR, "images", str(restaurant.pk))
                make_dir(dir_path)
                file_path = os.path.join(dir_path, "icon.jpg")
                write_image(file_path, data.get("icon"))
                icon_path = "images/{}/{}".format(restaurant.pk, "icon.jpg")
                restaurant.icon_path = icon_path
                restaurant.save()

            if data.get("photos"):
                dir_path = os.path.join(settings.BASE_DIR, "images", str(restaurant.pk))
                make_dir(dir_path)
                for photo in data.get("photos"):
                    file_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16)) + '.jpg'
                    file_path = os.path.join(dir_path, file_name)
                    write_image(file_path, photo)
                    image_path = "images/{}/{}".format(restaurant.pk, file_name)
                    RestaurantImage.objects.create(restaurant=restaurant, path=image_path)

            restaurant_id = restaurant.pk

        return restaurant_id


    def update(self, instance, validated_data, **kwargs):
        data = dict(self.validated_data, **kwargs)

        with transaction.atomic():
            instance.admin = validated_data.get('admin', instance.admin)
            instance.title = validated_data.get('title', instance.title)
            instance.average_check = validated_data.get('average_check', instance.average_check)
            instance.time_open = validated_data.get('time_open', instance.time_open)
            instance.time_close = validated_data.get('time_close', instance.time_close)
            instance.description = validated_data.get('description', instance.description)

            if data.get("icon"):
                if instance.icon_path:
                    file_path = os.path.join(settings.BASE_DIR, instance.icon_path)
                    delete_image(file_path)
                dir_path = os.path.join(settings.BASE_DIR, "images", str(instance.pk))
                make_dir(dir_path)
                file_path = os.path.join(dir_path, "icon.jpg")
                write_image(file_path, data.get("icon"))
                icon_path = "images/{}/{}".format(instance.pk, "icon.jpg")
                instance.icon_path = icon_path
            instance.save()

            if data.get("photos"):
                restaurant_images = list(RestaurantImage.objects.filter(restaurant=instance))
                for restaurant_image in restaurant_images:
                    restaurant_image.delete()
                dir_path = os.path.join(settings.BASE_DIR, "images", str(instance.pk))
                make_dir(dir_path)
                for photo in data.get("photos"):
                    file_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16)) + '.jpg'
                    file_path = os.path.join(dir_path, file_name)
                    write_image(file_path, photo)
                    image_path = "images/{}/{}".format(instance.pk, file_name)
                    RestaurantImage.objects.create(restaurant=instance, path=image_path)


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['restaurant', 'address']

    def save(self, **kwargs):
        data = dict(self.validated_data, **kwargs)

        with transaction.atomic():
            branch = Branch.objects.create(
                restaurant_id=data["restaurant"],
                address=data["address"]
            )

            if data.get("photos"):
                dir_path = os.path.join(settings.BASE_DIR, "images", str(branch.restaurant_id), str(branch.pk))
                make_dir(dir_path)
                for photo in data.get("photos"):
                    file_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16)) + '.jpg'
                    file_path = os.path.join(dir_path, file_name)
                    write_image(file_path, photo)
                    image_path = "images/{}/{}/{}".format(branch.restaurant_id, branch.pk, file_name)
                    BranchImage.objects.create(branch=branch, path=image_path)

            branch_id = branch.pk

        return branch_id


    def update(self, instance, **kwargs):
        data = dict(self.validated_data, **kwargs)

        with transaction.atomic():
            instance.restaurant_id = self.validated_data.get('restaurant', instance.restaurant_id)
            instance.address = self.validated_data.get('address', instance.address)

            if data.get("photos"):
                branch_images = list(BranchImage.objects.filter(branch=instance))
                for branch_image in branch_images:
                    branch_image.delete()
                dir_path = os.path.join(settings.BASE_DIR, "images", str(instance.restaurant_id), str(instance.pk))
                make_dir(dir_path)
                for photo in data.get("photos"):
                    file_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16)) + '.jpg'
                    file_path = os.path.join(dir_path, file_name)
                    write_image(file_path, photo)
                    image_path = "images/{}/{}/{}".format(instance.restaurant_id, instance.pk, file_name)
                    BranchImage.objects.create(branch=instance, path=image_path)
            instance.save()


class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ['restaurant', 'title']

    def save(self, **kwargs):
        data = dict(self.validated_data, **kwargs)

        with transaction.atomic():
            menu_category = MenuCategory.objects.create(
                restaurant_id=data["restaurant"],
                title=data["title"]
            )

            if data.get("photo"):
                dir_path = os.path.join(settings.BASE_DIR, "images", str(menu_category.restaurant_id), "menu")
                make_dir(dir_path)
                file_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16)) + '.jpg'
                file_path = os.path.join(dir_path, file_name)
                write_image(file_path, data.get("photo"))
                image_path = "images/{}/menu/{}".format(menu_category.restaurant_id, file_name)
                menu_category.image_path = image_path
                menu_category.save()

            menu_category_id = menu_category.pk

        return menu_category_id


    def update(self, instance, **kwargs):
        data = dict(self.validated_data, **kwargs)

        with transaction.atomic():
            instance.restaurant_id = self.validated_data.get('restaurant', instance.restaurant_id)
            instance.title = self.validated_data.get('title', instance.title)

            if data.get("photo"):
                if instance.image_path:
                    file_path = os.path.join(settings.BASE_DIR, instance.image_path)
                    delete_image(file_path)
                dir_path = os.path.join(settings.BASE_DIR, "images", str(instance.restaurant_id), "menu")
                make_dir(dir_path)
                file_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16)) + '.jpg'
                file_path = os.path.join(dir_path, file_name)
                write_image(file_path, data.get("photo"))
                image_path = "images/{}/menu/{}".format(instance.restaurant_id, file_name)
                instance.image_path = image_path
            instance.save()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['menu_category', 'title', 'bottom_price', 'top_price', 'description']

    def save(self, **kwargs):
        data = dict(self.validated_data, **kwargs)

        with transaction.atomic():
            product = Product.objects.create(
                menu_category_id=data["menu_category"],
                title=data["title"],
                bottom_price=data["bottom_price"],
                top_price=data["top_price"],
                description=data["description"]
            )

            if data.get("branch_ids"):
                branches = Branch.objects.filter(pk__in=data.get("branch_ids"))
                product.branches.set(branches)

            if data.get("photo"):
                dir_path = os.path.join(settings.BASE_DIR, "images", str(product.menu_category.restaurant_id), "menu")
                make_dir(dir_path)
                file_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16)) + '.jpg'
                file_path = os.path.join(dir_path, file_name)
                write_image(file_path, data.get("photo"))
                image_path = "images/{}/menu/{}".format(product.menu_category.restaurant_id, file_name)
                product.image_path = image_path
                product.save()

            product_id = product.pk

        return product_id


    def update(self, instance, **kwargs):
        data = dict(self.validated_data, **kwargs)

        with transaction.atomic():
            instance.menu_category_id = self.validated_data.get('menu_category', instance.menu_category_id)
            instance.title = self.validated_data.get('title', instance.title)
            instance.bottom_price = self.validated_data.get('bottom_price', instance.bottom_price)
            instance.top_price = self.validated_data.get('top_price', instance.top_price)
            instance.description = self.validated_data.get('description', instance.description)

            if data.get("branch_ids"):
                instance.branches.clear()
                branches = Branch.objects.filter(pk__in=data.get("branch_ids"))
                instance.branches.set(branches)

            if data.get("photo"):
                if instance.image_path:
                    file_path = os.path.join(settings.BASE_DIR, instance.image_path)
                    delete_image(file_path)
                dir_path = os.path.join(settings.BASE_DIR, "images", str(instance.branch.restaurant_id),
                                        str(instance.branch_id), "menu")
                make_dir(dir_path)
                file_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16)) + '.jpg'
                file_path = os.path.join(dir_path, file_name)
                write_image(file_path, data.get("photo"))
                image_path = "images/{}/{}/menu/{}".format(instance.branch.restaurant_id, instance.branch_id, file_name)
                instance.image_path = image_path
            instance.save()



def make_dir(dir_path):
    try:
        os.makedirs(dir_path)
    except OSError:
        print('Directory - {} exists'.format(dir_path))


def write_image(file_path, image):
    with open(file_path, 'wb+') as file:
        for chunk in image.chunks():
            file.write(chunk)


def delete_image(file_path):
    try:
        os.remove(file_path)
    except OSError:
        pass