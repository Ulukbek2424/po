# Generated by Django 4.2.2 on 2023-06-24 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='branchimage',
            old_name='url',
            new_name='path',
        ),
        migrations.RenameField(
            model_name='menucategory',
            old_name='image_url',
            new_name='image_path',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='image_url',
            new_name='image_path',
        ),
        migrations.RenameField(
            model_name='restaurant',
            old_name='icon_url',
            new_name='icon_path',
        ),
        migrations.RenameField(
            model_name='restaurantimage',
            old_name='url',
            new_name='path',
        ),
    ]