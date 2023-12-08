import django_tables2 as tables

from stock.models import Stock


class StockTable(tables.Table):
    details = tables.TemplateColumn('<a href="{% url \'stock-detail\' record.id %}">&#128203;</a>',
                                    orderable=False, verbose_name="")

    class Meta:
        model = Stock
        template_name = "django_tables2/bootstrap.html"
        fields = ('details', 'name', 'address')
