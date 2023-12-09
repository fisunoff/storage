import json
from random import randint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django_tables2 import SingleTableView

from mixins import AddTitleFormMixin, ProDetailView, SaveEditorMixin, DetailWithSingleTable
from operation.const import ADMISSION, DEPARTURE, RECALC
from operation.models import Operation
from operation.tables import  OperationByProductTable
from product.models import Product
from product.tables import ProductTable


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
        stocks = {}
        operations = Operation.objects.filter(product=self.object)
        for elem in operations:
            if elem.type in (ADMISSION, DEPARTURE, RECALC):
                if elem.stock.name not in stocks:
                    stocks[elem.stock.name] = 0
                if elem.type in (ADMISSION, RECALC):
                    stocks[elem.stock.name] += elem.quantity
                else:
                    stocks[elem.stock.name] += elem.quantity
            else:
                if elem.from_stock.name not in stocks:
                    stocks[elem.from_stock.name] = 0
                if elem.to_stock.name not in stocks:
                    stocks[elem.to_stock.name] = 0
                stocks[elem.from_stock.name] -= elem.quantity
                stocks[elem.to_stock.name] += elem.quantity

        diagram_labels = []
        diagram_data = []
        for stock in stocks:
            if stocks[stock] > 0:
                diagram_labels.append(stock)
                diagram_data.append(stocks[stock])

        kwargs['diagram_labels'] = json.dumps(diagram_labels)
        kwargs['diagram_data'] = diagram_data
        kwargs['colors'] = [
            f'rgba({randint(50, 200)}, {randint(50, 200)}, {randint(50, 200)}, 0.7)' for i in range(len(diagram_data))
        ]
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
