from io import BytesIO

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django_tables2 import SingleTableView

from extended_user.models import Profile
from mixins import AddTitleFormMixin, SaveEditorMixin
from report.models import Report
from report.tables import ReportTable
from report.worker import make_report


class ReportCreateView(LoginRequiredMixin, SaveEditorMixin, AddTitleFormMixin, CreateView):
    model = Report
    template_name = 'base_create.html'

    fields = ('start_date', 'end_date')
    title = "Генерация отчета"

    def get_initial(self):
        initial_data = {}
        for i in self.fields:
            initial_data[i] = self.request.GET.get(i)
        return initial_data

    def get_success_url(self):
        return reverse_lazy('report-list')

    def form_valid(self, form):
        self.object = form.save()
        user_profile = Profile.objects.get(id=self.request.user.profile.id)
        if not self.save_creator_only:
            self.object.last_editor = user_profile
        if not self.object.creator:
            self.object.creator = user_profile
        self.object.save()
        make_report.send(self.object.pk)
        return HttpResponseRedirect(self.get_success_url())


class ReportListView(SingleTableView):

    model = Report
    template_name = 'report/list.html'
    table_class = ReportTable

    def get_context_data(self, **kwargs):
        can_edit = self.request.user.is_authenticated
        kwargs['can_edit'] = can_edit
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-id')
        return qs


def download_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if report.file:
        return FileResponse(report.file, as_attachment=True, filename=report.file.name)
    else:
        return HttpResponse("Файл отчета не найден", status=404)
