import django_tables2 as tables

from product.models import Product


class ProductTable(tables.Table):
    details = tables.TemplateColumn('<a href="{% url \'product-detail\' record.id %}">&#128203;</a>',
                                    orderable=False, verbose_name="")

    class Meta:
        model = Product
        template_name = "django_tables2/bootstrap.html"
        fields = ('details', 'name', 'measure_type')
