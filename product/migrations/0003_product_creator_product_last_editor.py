# Generated by Django 5.0 on 2023-12-08 10:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extended_user', '0001_initial'),
        ('product', '0002_alter_product_options_alter_product_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products_by_creator', to='extended_user.profile', verbose_name='Создатель'),
        ),
        migrations.AddField(
            model_name='product',
            name='last_editor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products_by_last_editor', to='extended_user.profile', verbose_name='Последний редактор'),
        ),
    ]
