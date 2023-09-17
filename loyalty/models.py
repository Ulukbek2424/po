# import os
# from django.db import models
# from django.conf import settings
#
# from restaurant.models import Restaurant, Waiter
#
#
# class Promotion(models.Model):
#     restaurant = models.ForeignKey(Restaurant, null=True, default=None, on_delete=models.CASCADE)
#     title = models.CharField(max_length=128, default="")
#     image_path = models.CharField(max_length=128, null=True, default=None)
#     description = models.TextField(null=True, default=None)
#     expiration_date = models.DateField()
