from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField("Имя", max_length=50, blank=False, null=True)
    surname = models.CharField("Фамилия", max_length=50, blank=False, null=True)
    patronymic = models.CharField("Отчество", max_length=50, blank=True, null=True)
    bio = models.TextField("Описание профиля", max_length=500, blank=True, null=True)
    university = models.CharField(verbose_name="Место учебы", max_length=200, blank=True, null=True)
    communication = models.CharField(verbose_name="Другие способы коммуникации", max_length=200, blank=True, null=True)
    time_create = models.DateTimeField(verbose_name="Дата создания учетной записи", default=timezone.now)
    photo = models.ImageField(verbose_name="Фото профиля", blank=True, null=True)

    def __str__(self):
        return f"{self.surname} {self.name}{' ' + self.patronymic if self.patronymic else ''}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        unique_together = ['name', 'surname', 'patronymic']
        # ordering = ['surname', 'name', 'position']


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
