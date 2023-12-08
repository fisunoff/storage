from django.db import models
from django.db.models.functions import datetime

from extended_user.models import Profile


class Operation(models.Model):
    operations = (
        ('admission', 'Поступление'),
        ('departure', 'Убытие'),
        ('transfer', 'Передача'),
        ('recalc', 'Переучет')
    )
    operations_dict = dict(operations)
    type = models.CharField(choices=operations, max_length=1024)
    product = models.ForeignKey(to='product.Product', on_delete=models.PROTECT)
    quantity = models.FloatField(verbose_name='Количество')
    price = models.FloatField(verbose_name='Цена')
    cost = models.FloatField(verbose_name='Стоимость')
    creator = models.ForeignKey(to=Profile, on_delete=models.SET_NULL, null=True, related_name='operations_by_creator',
                                verbose_name='Создатель')
    last_editor = models.ForeignKey(to=Profile, on_delete=models.SET_NULL, null=True,
                                    related_name='operations_by_editor',
                                    verbose_name='Последний редактор')
    from_stock = models.ForeignKey(to='stock.Stock', on_delete=models.SET_NULL, null=True, related_name='from_stocks',
                                   verbose_name='Исходный склад')
    to_stock = models.ForeignKey(to='stock.Stock', on_delete=models.SET_NULL, null=True, related_name='to_stocks',
                                 verbose_name='Новый склад')
    stock = models.ForeignKey(to='stock.Stock', on_delete=models.SET_NULL, null=True, related_name='stocks',
                              verbose_name='Склад')
    time_create = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Время создания')
    date = models.DateField(verbose_name='Дата операции')

    class Meta:
        verbose_name = "Операция"
        verbose_name_plural = "Операции"
        default_related_name = 'operations'

    def __str__(self):
        return f"{self.operations_dict[self.type]} ресурса {self.product} от {self.date}"
