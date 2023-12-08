from django.db import models
from django.db.models import Value
from django.db.models.functions import Concat

from extended_user.models import Profile
from storage.settings import MEDIA_URL


class ReportManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs


class Report(models.Model):
    statuses = (
        ('in_progress', 'Генерация'),
        ('OK', 'Сгенерирован'),
        ('error', 'Ошибка генерации')
    )

    objects = ReportManager()

    creator = models.ForeignKey(to=Profile, on_delete=models.SET_NULL, null=True, related_name='reports_by_creator',
                                verbose_name='Создатель')
    start_date = models.DateField(verbose_name='От')
    end_date = models.DateField(verbose_name='До')
    status = models.CharField(max_length=1024, verbose_name='Статус', choices=statuses, default='in_progress')
    file = models.FileField(verbose_name='Файл')

    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"

    def __str__(self):
        return f"С {self.start_date} по {self.end_date}"
