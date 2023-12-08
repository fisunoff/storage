from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django_tables2 import SingleTableView

from mixins import AddTitleFormMixin, ProDetailView, SaveEditorMixin
from operation.const import ADMISSION, DEPARTURE, TRANSFER, RECALC
from operation.filters import OperationFilter
from operation.models import Operation
from operation.tables import OperationTable


class OperationCreateView(LoginRequiredMixin, SaveEditorMixin, AddTitleFormMixin, CreateView):
    model = Operation
    template_name = 'base_create.html'

    fields = ('type', 'product', 'quantity', 'price', 'cost', 'from_stock', 'to_stock', 'stock', 'date')
    title = "Добавление операции"

    def get_initial(self):
        initial_data = {}
        for i in self.fields:
            initial_data[i] = self.request.GET.get(i)
        return initial_data

    def get_success_url(self):
        return reverse_lazy('operation-detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        # cost = quantity * price
        quantity = form.cleaned_data.get('quantity', None)
        price = form.cleaned_data.get('price', None)
        cost = form.cleaned_data.get('cost', None)
        type = form.cleaned_data.get('type', None)
        if type is None:
            return super().form_valid(form)

        if type in (ADMISSION, DEPARTURE, RECALC):
            form.cleaned_data['from_stock'] = None
            form.cleaned_data['to_stock'] = None
            form.instance.from_stock = None
            form.instance.to_stock = None
            if form.cleaned_data['stock'] is None:
                form.add_error('price',
                               'Должно быть заполнено поле склад')
                return self.form_invalid(form)

        if type == TRANSFER:
            form.cleaned_data['stock'] = None
            form.instance.stock = None
            if form.cleaned_data['from_stock'] is None or form.cleaned_data['to_stock'] is None:
                form.add_error('price',
                               'Должны быть заполнены поля Исходный склад и Новый склад')
                return self.form_invalid(form)


        if price is None:
            if cost is None or quantity is None:
                form.add_error('price',
                               f'Должно быть заполнено 2 поля из 3: Количество, Цена, Стоимость')
                return self.form_invalid(form)
            form.cleaned_data['price'] = cost / quantity
            form.instance.price = cost / quantity
            return super().form_valid(form)

        if cost is None:
            if price is None or quantity is None:
                form.add_error('price',
                               f'Должно быть заполнено 2 поля из 3: Количество, Цена, Стоимость')
                return self.form_invalid(form)
            form.cleaned_data['cost'] = quantity * price
            form.instance.cost = quantity * price
            return super().form_valid(form)

        if quantity is None:
            if cost is None or quantity is None:
                form.add_error('price',
                               f'Должно быть заполнено 2 поля из 3: Количество, Цена, Стоимость')
                return self.form_invalid(form)
            form.cleaned_data['quantity'] = cost / price
            form.instance.quantity = cost / price
            return super().form_valid(form)

        form.add_error('price',
                       f'Должно быть заполнено 2 поля из 3: Количество, Цена, Стоимость')
        return self.form_invalid(form)


class OperationDetailView(ProDetailView):
    model = Operation
    template_name = 'operation/detail.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        can_edit = False
        if self.request.user.is_authenticated:
            can_edit = self.request.user.profile.pk == self.object.creator or self.request.user.is_superuser
        kwargs['type_name'] = Operation.operations_dict[self.object.type]
        kwargs['can_edit'] = can_edit
        kwargs['from_and_to'] = (self.object.type == TRANSFER)
        return kwargs


class OperationUpdateView(SaveEditorMixin, LoginRequiredMixin, AddTitleFormMixin, UpdateView):
    model = Operation
    template_name = 'base_create.html'

    fields = ('type', 'product', 'quantity', 'price', 'cost', 'from_stock', 'to_stock', 'stock', 'date')
    title = "Редактирование операции"
    editing = True

    def get_success_url(self):
        return reverse_lazy('operation-detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        # cost = quantity * price
        quantity = form.cleaned_data.get('quantity', None)
        price = form.cleaned_data.get('price', None)
        cost = form.cleaned_data.get('cost', None)
        type = form.cleaned_data.get('type', None)
        if type is None:
            return super().form_valid(form)

        if type in (ADMISSION, DEPARTURE, RECALC):
            form.cleaned_data['from_stock'] = None
            form.cleaned_data['to_stock'] = None
            form.instance.from_stock = None
            form.instance.to_stock = None
            if form.cleaned_data['stock'] is None:
                form.add_error('price',
                               'Должно быть заполнено поле склад')
                return self.form_invalid(form)

        if type == TRANSFER:
            form.cleaned_data['stock'] = None
            form.instance.stock = None
            if form.cleaned_data['from_stock'] is None or form.cleaned_data['to_stock'] is None:
                form.add_error('price',
                               'Должны быть заполнены поля Исходный склад и Новый склад')
                return self.form_invalid(form)

        if price is None:
            if cost is None or quantity is None:
                form.add_error('price',
                               f'Должно быть заполнено 2 поля из 3: Количество, Цена, Стоимость')
                return self.form_invalid(form)
            form.cleaned_data['price'] = cost / quantity
            form.instance.price = cost / quantity
            return super().form_valid(form)

        if cost is None:
            if price is None or quantity is None:
                form.add_error('price',
                               f'Должно быть заполнено 2 поля из 3: Количество, Цена, Стоимость')
                return self.form_invalid(form)
            form.cleaned_data['cost'] = quantity * price
            form.instance.cost = quantity * price
            return super().form_valid(form)

        if quantity is None:
            if cost is None or quantity is None:
                form.add_error('price',
                               f'Должно быть заполнено 2 поля из 3: Количество, Цена, Стоимость')
                return self.form_invalid(form)
            form.cleaned_data['quantity'] = cost / price
            form.instance.quantity = cost / price
            return super().form_valid(form)

        form.add_error('price',
                       f'Должно быть заполнено 2 поля из 3: Количество, Цена, Стоимость')
        return self.form_invalid(form)


class OperationListView(SingleTableView):

    model = Operation
    template_name = 'base_list.html'
    table_class = OperationTable

    def get_context_data(self, **kwargs):
        can_edit = self.request.user.is_authenticated
        kwargs['can_edit'] = can_edit
        kwargs['filter'] = OperationFilter
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        args = self.request.GET
        if args.get('stock__name__contains', None):
            qs = qs.filter(stock_name__icontains=args['stock__name__contains'])
        if args.get('type', None):
            qs = qs.filter(type=args['type'])
        return qs
