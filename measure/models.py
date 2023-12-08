from django.db import models
from django.db.models import SET_NULL

from extended_user.models import Profile


# Create your models here.
class Measure(models.Model):
    name = models.CharField(max_length=1024, verbose_name='Наименование')
    creator = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='measures_by_creator',
                                verbose_name='Создатель')
    last_editor = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='measures_by_last_editor',
                                    verbose_name='Последний редактор')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерения"
        unique_together = ['name', ]
