import copy
import os

import dramatiq
from django.core.files import File
from django.db.models import Q
from django.utils.timezone import now

from utils import generate_report, TableReport

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
    from operation.const import ADMISSION, DEPARTURE, RECALC
    from product.models import Product
    report = Report.objects.get(pk=pk)

    # region table_total

    operations = Operation.objects.filter(Q(date__gte=report.start_date) & Q(date__lte=report.end_date))
    data = list()
    products_at_start = {}
    for product in Product.objects.all():
        products_at_start[product.name] = 0

    before_operations = Operation.objects.filter(date__lt=report.start_date)
    for operation in before_operations:
        if operation.type in (ADMISSION, RECALC):
            products_at_start[operation.product.name] += operation.quantity
        if operation.type == DEPARTURE:
            products_at_start[operation.product.name] -= operation.quantity

    products_at_end = copy.deepcopy(products_at_start)

    for obj in operations:
        elem = {
            "type": str(obj.product),
            "type_of_operation": obj.type_str,
            "date": obj.date,
            "stock": obj.stock_name,
            "count": obj.quantity,
            "unit": obj.measure,
            "price": obj.price,
            "sum": obj.cost
        }
        data.append(elem)
        if obj.type in (ADMISSION, RECALC):
            products_at_end[obj.product.name] += obj.quantity
        if obj.type == DEPARTURE:
            products_at_end[obj.product.name] -= obj.quantity

    final_data = []

    for key in products_at_start:
        elem = {
            'type': key,
            'start': products_at_start[key],
            'end': products_at_end[key],
            'diff': products_at_end[key] - products_at_start[key],
        }
        final_data.append(elem)

    final_table = TableReport(
        col_names=["Продукт", "Количество на начало периода", "Количество на конец периода", 'Разница'],
        data=final_data,
        report_name='Краткий отчет по всем ресурсам'
    )

    table_total = TableReport(
        col_names=["Продукт", "Тип операции", "Дата", "Склад", "Количество", "Единица измерения", "Цена за единицу",
                   "Сумма"],
        data=data,
        report_name='Отчет по всем операциям'
    )

    # endregion table_total

    # region table_sales
    operations = Operation.objects.filter(
        Q(date__gte=report.start_date)
        & Q(date__lte=report.end_date)
        & Q(type=DEPARTURE)
    )
    data = list()

    for obj in operations:
        elem = {
            "type": str(obj.product),
            "date": obj.date,
            "stock": obj.stock_name,
            "count": obj.quantity,
            "unit": obj.measure,
            "price": obj.price,
            "sum": obj.cost
        }
        data.append(elem)

    table_sales = TableReport(
        col_names=["Продукт", "Дата", "Склад", "Количество", "Единица измерения", "Цена за единицу", "Сумма"],
        data=data,
        report_name='Отчет по продажам'
    )

    # endregion table_sales

    # region table_admission
    operations = Operation.objects.filter(
        Q(date__gte=report.start_date)
        & Q(date__lte=report.end_date)
        & Q(type=ADMISSION)
    )
    data = list()

    for obj in operations:
        elem = {
            "type": str(obj.product),
            "date": obj.date,
            "stock": obj.stock_name,
            "count": obj.quantity,
            "unit": obj.measure,
            "price": obj.price,
            "sum": obj.cost
        }
        data.append(elem)

    table_admission = TableReport(
        col_names=["Продукт", "Дата", "Склад", "Количество", "Единица измерения", "Цена за единицу", "Сумма"],
        data=data,
        report_name='Отчет по добыче'
    )

    # endregion table_sales

    doc_info = {"start_data": report.start_date,
                "end_data": report.end_date,
                "signature": str(report.creator)}

    filename = generate_report([table_total, final_table, table_sales, table_admission], doc_info)
    report.file = File(open(filename, 'rb'))
    report.file.filename = f'Отчет с {report.start_date} по {report.end_date}'
    report.status = 'OK'
    report.time_generated = now()
    report.save()
