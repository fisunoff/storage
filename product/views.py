from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django_tables2 import SingleTableView

from mixins import AddTitleFormMixin, ProDetailView, SaveEditorMixin, DetailWithSingleTable
from operation.filters import OperationFilter
from operation.models import Operation
from operation.tables import SmallOperationTable, OperationByProductTable
from product.models import Product
from product.tables import ProductTable
from stock.models import Stock
from stock.tables import StockTable


class ProductCreateView(LoginRequiredMixin, SaveEditorMixin, AddTitleFormMixin, CreateView):
    model = Product
    template_name = 'base_create.html'

    fields = ('name', 'measure_type')
    title = "Добавление ресурса"

    def get_initial(self):
        initial_data = {}
        for i in self.fields:
            initial_data[i] = self.request.GET.get(i)
        return initial_data

    def get_success_url(self):
        return reverse_lazy('product-detail', kwargs={'pk': self.object.id})


class ProductDetailView(DetailWithSingleTable):
    model = Product
    template_name = 'product/detail.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        can_edit = False
        if self.request.user.is_authenticated:
            can_edit = self.request.user.profile.pk == self.object.creator or self.request.user.is_superuser
        kwargs['can_edit'] = can_edit
        return kwargs

    table_model = Operation
    table_class = OperationByProductTable

    def get_table_data(self):
        product = self.object.id
        product_obj = Product.objects.get(pk=product)
        if not self.request.user.is_authenticated:
            return self.table_model.objects.none()
        else:
            return self.table_model.objects.filter(
                product=product_obj
            )


class ProductUpdateView(SaveEditorMixin, LoginRequiredMixin, AddTitleFormMixin, UpdateView):
    model = Product
    template_name = 'base_create.html'

    fields = ('name', 'measure_type')
    title = "Редактирование ресурса"
    editing = True

    def get_success_url(self):
        return reverse_lazy('product-detail', kwargs={'pk': self.object.id})


class ProductListView(SingleTableView):

    model = Product
    template_name = 'product/list.html'
    table_class = ProductTable

    def get_context_data(self, **kwargs):
        can_edit = self.request.user.is_authenticated
        kwargs['can_edit'] = can_edit
        return super().get_context_data(**kwargs)
