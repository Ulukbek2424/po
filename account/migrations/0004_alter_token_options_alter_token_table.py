# Generated by Django 4.2.2 on 2023-06-21 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_token'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='token',
            options={'verbose_name': 'Token', 'verbose_name_plural': 'Token'},
        ),
        migrations.AlterModelTable(
            name='token',
            table='token',
        ),
    ]
