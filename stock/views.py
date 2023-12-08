from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django_tables2 import SingleTableView

from mixins import AddTitleFormMixin, ProDetailView, SaveEditorMixin, DetailWithSingleTable
from operation.filters import OperationFilter
from operation.models import Operation
from operation.tables import SmallOperationTable
from stock.models import Stock
from stock.tables import StockTable


class StockCreateView(LoginRequiredMixin, SaveEditorMixin, AddTitleFormMixin, CreateView):
    model = Stock
    template_name = 'base_create.html'

    fields = ('name', 'address')
    title = "Добавление склада"

    def get_initial(self):
        initial_data = {}
        for i in self.fields:
            initial_data[i] = self.request.GET.get(i)
        return initial_data

    def get_success_url(self):
        return reverse_lazy('stock-detail', kwargs={'pk': self.object.id})


class StockDetailView(DetailWithSingleTable):
    model = Stock
    template_name = 'stock/detail.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        can_edit = False
        if self.request.user.is_authenticated:
            can_edit = self.request.user.profile.pk == self.object.creator or self.request.user.is_superuser
        kwargs['can_edit'] = can_edit
        return kwargs

    table_model = Operation
    table_class = SmallOperationTable

    def get_table_data(self):
        stock = self.object.id
        stock_obj = Stock.objects.get(pk=stock)
        if not self.request.user.is_authenticated:
            return self.table_model.objects.none()
        else:
            return self.table_model.objects.filter(
                models.Q(stock=stock_obj)
                | models.Q(from_stock=stock_obj)
                | models.Q(to_stock=stock_obj)
            )


class StockUpdateView(SaveEditorMixin, LoginRequiredMixin, AddTitleFormMixin, UpdateView):
    model = Stock
    template_name = 'base_create.html'

    fields = ('name', 'address')
    title = "Редактирование склада"
    editing = True

    def get_success_url(self):
        return reverse_lazy('stock-detail', kwargs={'pk': self.object.id})


class StockListView(SingleTableView):

    model = Stock
    template_name = 'stock/list.html'
    table_class = StockTable

    def get_context_data(self, **kwargs):
        can_edit = self.request.user.is_authenticated
        kwargs['can_edit'] = can_edit
        kwargs['filter'] = OperationFilter
        return super().get_context_data(**kwargs)
