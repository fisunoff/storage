import django_tables2 as tables

from operation.models import Operation


class OperationTable(tables.Table):
    details = tables.TemplateColumn('<a href="{% url \'operation-detail\' record.id %}">&#128203;</a>',
                                    orderable=False, verbose_name="")

    type_str = tables.Column(orderable=True, verbose_name="Тип")

    class Meta:
        model = Operation
        template_name = "django_tables2/bootstrap.html"
        fields = ('details', 'type_str', 'product', )