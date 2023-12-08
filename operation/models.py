from django.db import models
from django.db.models.functions import datetime

from extended_user.models import Profile
from operation.const import ADMISSION, DEPARTURE, TRANSFER, RECALC


class OperationManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('product').select_related('product__measure_type')
        qs = qs.annotate(type_str=models.Case(
            models.When(
                models.Q(type=ADMISSION),
                then=models.Value('Поступление')
            ),
            models.When(
                models.Q(type=DEPARTURE),
                then=models.Value('Продажа')
            ),
            models.When(
                models.Q(type=TRANSFER),
                then=models.Value('Передача')
            ),
            models.When(
                models.Q(type=RECALC),
                then=models.Value('Переучет')
            ),
            default=models.Value('Не определено'),
            output_field=models.CharField(max_length=1024)
            ),
            measure=models.F('product__measure_type__name'),
        )
        return qs


class Operation(models.Model):
    operations = (
        (ADMISSION, 'Поступление'),
        (DEPARTURE, 'Продажа'),
        (TRANSFER, 'Передача'),
        (RECALC, 'Переучет')
    )

    objects = OperationManager()

    operations_dict = dict(operations)
    type = models.CharField(choices=operations, max_length=1024, verbose_name='Операция')
    product = models.ForeignKey(to='product.Product', on_delete=models.PROTECT, verbose_name='Ресурс')
    quantity = models.FloatField(verbose_name='Количество', null=True, blank=True,)
    price = models.FloatField(verbose_name='Цена', null=True, blank=True,)
    cost = models.FloatField(verbose_name='Стоимость', null=True, blank=True,)
    creator = models.ForeignKey(to=Profile, on_delete=models.SET_NULL, null=True, related_name='operations_by_creator',
                                verbose_name='Создатель')
    last_editor = models.ForeignKey(to=Profile, on_delete=models.SET_NULL, null=True,
                                    related_name='operations_by_editor',
                                    verbose_name='Последний редактор')
    from_stock = models.ForeignKey(to='stock.Stock', on_delete=models.SET_NULL, null=True, blank=True, related_name='from_stocks',
                                   verbose_name='Исходный склад')
    to_stock = models.ForeignKey(to='stock.Stock', on_delete=models.SET_NULL, null=True, blank=True, related_name='to_stocks',
                                 verbose_name='Новый склад')
    stock = models.ForeignKey(to='stock.Stock', on_delete=models.SET_NULL, null=True, blank=True, related_name='stocks',
                              verbose_name='Склад')
    time_create = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Время создания')
    date = models.DateField(verbose_name='Дата операции')

    class Meta:
        verbose_name = "Операция"
        verbose_name_plural = "Операции"
        default_related_name = 'operations'

    def __str__(self):
        return f"{self.operations_dict[self.type]} ресурса {self.product} от {self.date}"

    @property
    def quantity_str(self):
        return f"{self.quantity} {str(self.product.measure_type)}"
