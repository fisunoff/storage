from django_filters import FilterSet

from operation.models import Operation


class OperationFilter(FilterSet):
    class Meta:
        model = Operation
        fields = ("stock", "type")


class SmallOperationFilter(FilterSet):
    class Meta:
        model = Operation
        fields = {"type": ["exact"], "product": ["exact"], }