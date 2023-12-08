from django.db import models
from django.db.models import SET_NULL

from extended_user.models import Profile


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=1024, verbose_name='Наименование')
    measure_type = models.ForeignKey(to='measure.Measure', on_delete=models.PROTECT, verbose_name='Единица измерения')
    creator = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='products_by_creator',
                                verbose_name='Создатель')
    last_editor = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='products_by_last_editor',
                                    verbose_name='Последний редактор')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ресурс"
        verbose_name_plural = "Ресурсы"
        unique_together = ['name', ]
