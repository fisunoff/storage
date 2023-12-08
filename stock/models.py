from django.db import models
from django.db.models import SET_NULL

from extended_user.models import Profile


# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=1024, verbose_name='Наименование')
    address = models.CharField(max_length=1024, verbose_name='Адрес')
    creator = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='stocks_by_creator',
                                verbose_name='Создатель')
    last_editor = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='stocks_by_last_editor',
                                    verbose_name='Последний редактор')

    def __str__(self):
        return f"{self.name} ({self.address})"

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"
        unique_together = ['name', 'address']
