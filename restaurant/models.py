import os
from django.db import models
from django.conf import settings

from account.models import Admin, Waiter


class Restaurant(models.Model):
    admin = models.ForeignKey(Admin, null=True, default=None, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, default="", unique=True)
    icon_path = models.CharField(max_length=128, null=True, default=None)
    average_check = models.IntegerField(null=True, default=None)
    time_open = models.TimeField(auto_now=False, auto_now_add=False, null=True, default=None)
    time_close = models.TimeField(auto_now=False, auto_now_add=False, null=True, default=None)
    description = models.TextField(null=True, default=None)

    def delete(self, *args, **kwargs):
        if self.icon_path:
            file_path = os.path.join(settings.BASE_DIR, self.icon_path)
            if os.path.exists(file_path):
                os.remove(file_path)

        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'
        db_table = 'restaurant'


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, null=True, default=None, on_delete=models.CASCADE)
    path = models.CharField(max_length=128, null=True, default=None)

    def delete(self, *args, **kwargs):
        if self.path:
            file_path = os.path.join(settings.BASE_DIR, self.path)
            if os.path.exists(file_path):
                os.remove(file_path)

        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'RestaurantImage'
        verbose_name_plural = 'RestaurantImages'
        db_table = 'restaurant_image'


class Branch(models.Model):
    restaurant = models.ForeignKey(Restaurant, null=True, default=None, on_delete=models.CASCADE)
    address = models.CharField(max_length=128, null=True, default=None)
    waiters = models.ManyToManyField(Waiter)

    class Meta:
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'
        db_table = 'branch'
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'address'], name='unique_restaurant_address_combination')
        ]


class BranchImage(models.Model):
    branch = models.ForeignKey(Branch, null=True, default=None, on_delete=models.CASCADE)
    path = models.CharField(max_length=128, null=True, default=None)

    def delete(self, *args, **kwargs):
        if self.path:
            file_path = os.path.join(settings.BASE_DIR, self.path)
            if os.path.exists(file_path):
                os.remove(file_path)

        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'BranchImage'
        verbose_name_plural = 'BranchImages'
        db_table = 'branch_image'


class MenuCategory(models.Model):
    restaurant = models.ForeignKey(Restaurant, null=True, default=None, on_delete=models.CASCADE)
    title = models.CharField(max_length=32, default="")
    image_path = models.CharField(max_length=128, null=True, default=None)

    def delete(self, *args, **kwargs):
        if self.image_path:
            file_path = os.path.join(settings.BASE_DIR, self.image_path)
            if os.path.exists(file_path):
                os.remove(file_path)

        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'MenuCategory'
        verbose_name_plural = 'MenuCategories'
        db_table = 'menu_category'
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'title'], name='unique_restaurant_title_combination')
        ]


class Product(models.Model):
    menu_category = models.ForeignKey(MenuCategory, null=True, default=None, on_delete=models.CASCADE)
    branches = models.ManyToManyField(Branch)
    title = models.CharField(max_length=64, default="")
    bottom_price = models.IntegerField(null=True, default=None)
    top_price = models.IntegerField(null=True, default=None)
    description = models.TextField(null=True, default=None)
    image_path = models.CharField(max_length=128, null=True, default=None)

    def delete(self, *args, **kwargs):
        if self.image_path:
            file_path = os.path.join(settings.BASE_DIR, self.image_path)
            if os.path.exists(file_path):
                os.remove(file_path)

        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = 'product'
