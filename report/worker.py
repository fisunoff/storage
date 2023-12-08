import os

import dramatiq
from django.core.files import File
from django.db.models import Q

from utils import generate_report

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "storage.settings")

import django
django.setup()


from dramatiq.brokers.redis import RedisBroker
broker = RedisBroker()
dramatiq.set_broker(broker)

@dramatiq.actor
def make_report(pk):
    from report.models import Report
    from operation.models import Operation
    report = Report.objects.get(pk=pk)
    names_of_col = ["Продукт", "Тип операции", "Дата", "Склад", "Количество", "Единица измерения", "Цена за единицу", "Сумма"]
    operations = Operation.objects.filter(Q(date__gte=report.start_date) & Q(date__lte=report.end_date))
    data = list()
    for obj in operations:
        elem = {
            "type": str(obj.product),
            "type_of_operation": obj.type_str,
            "date": obj.date,
            "stock": obj.stock,
            "count": obj.quantity,
            "unit": obj.measure,
            "price": obj.price,
            "sum": obj.cost
        }
        data.append(elem)
    doc_info = {"start_data": report.start_date,
                "end_data": report.end_date,
                "signature": "Иванов А. П."}
    filename = generate_report(len(data), len(names_of_col), names_of_col, data, doc_info)
    report.file = File(open(filename, 'rb'))
    report.file.filename = f'Отчет с {report.start_date} по {report.end_date}'
    report.status = 'OK'
    report.save()
