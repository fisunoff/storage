from django.db import models

from extended_user.models import Profile


# Create your models here.

class Report(models.Model):
    statuses = (
        ('in_progress', 'Генерация'),
        ('OK', 'Сгенерирован'),
        ('error', 'Ошибка генерации')
    )
    creator = models.ForeignKey(to=Profile, on_delete=models.SET_NULL, null=True, related_name='reports_by_creator',
                                verbose_name='Создатель')
    start_date = models.DateField(verbose_name='С')
    end_date = models.DateField(verbose_name='По')
    status = models.CharField(max_length=1024, verbose_name='Статус', choices=statuses)
    file = models.FileField(verbose_name='Файл')

    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"

    def __str__(self):
        return f"С {self.start_date} по {self.end_date}"
