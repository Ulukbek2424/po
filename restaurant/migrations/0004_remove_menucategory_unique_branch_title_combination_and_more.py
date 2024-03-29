# Generated by Django 4.2.2 on 2023-07-06 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_alter_restaurant_icon_path'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='menucategory',
            name='unique_branch_title_combination',
        ),
        migrations.RemoveField(
            model_name='menucategory',
            name='branch',
        ),
        migrations.AddField(
            model_name='menucategory',
            name='restaurant',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant'),
        ),
        migrations.AddField(
            model_name='product',
            name='branches',
            field=models.ManyToManyField(to='restaurant.branch'),
        ),
        migrations.AddConstraint(
            model_name='menucategory',
            constraint=models.UniqueConstraint(fields=('restaurant', 'title'), name='unique_restaurant_title_combination'),
        ),
    ]
