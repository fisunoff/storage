# Generated by Django 5.0 on 2023-12-08 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extended_user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='university',
        ),
        migrations.AddField(
            model_name='profile',
            name='post',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Должность'),
        ),
    ]
