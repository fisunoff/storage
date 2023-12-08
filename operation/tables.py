import django_tables2 as tables

from operation.models import Operation


class OperationTable(tables.Table):
    details = tables.TemplateColumn('<a href="{% url \'operation-detail\' record.id %}">&#128203;</a>',
                                    orderable=False, verbose_name="")

    type_str = tables.Column(orderable=True, verbose_name="Тип")
    measure = tables.Column(orderable=True, verbose_name="Единица измерения")
    stock_name = tables.Column(orderable=True, verbose_name="Склад")

    class Meta:
        model = Operation
        template_name = "django_tables2/bootstrap.html"
        fields = ('details', 'stock_name', 'type_str', 'product', 'quantity', 'measure', 'date', )


class SmallOperationTable(OperationTable):
    class Meta:
        model = Operation
        template_name = "django_tables2/bootstrap.html"
        fields = ('details', 'type_str', 'product', 'quantity', 'measure', 'date', )

