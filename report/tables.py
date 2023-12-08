import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from report.models import Report


class ReportTable(tables.Table):
    download = tables.Column(orderable=False, verbose_name="", empty_values=())

    class Meta:
        model = Report
        template_name = "django_tables2/bootstrap.html"
        fields = ('download', 'start_date', 'end_date', 'status')

    def render_download(self, value, record):
        if self.request.user.is_authenticated and record.status == 'OK':
            url = reverse('report-download') + "?id=" + str(record.id)
            return format_html('<a href="{}"> <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16"><path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5"/><path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/></svg></a>', url)
        return ''
