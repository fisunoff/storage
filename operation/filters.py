from django_filters import FilterSet

from operation.models import Operation


class OperationFilter(FilterSet):
    class Meta:
        model = Operation
        fields = {"stock__name": ["contains"], "type": ["exact"]}


class SmallOperationFilter(FilterSet):
    class Meta:
        model = Operation
        fields = {"type": ["exact"], "product": ["exact"], }