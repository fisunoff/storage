# Generated by Django 5.0 on 2023-12-08 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Ресурс', 'verbose_name_plural': 'Ресурсы'},
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('name',)},
        ),
    ]
