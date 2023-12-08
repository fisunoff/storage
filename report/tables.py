import django_tables2 as tables
from django.utils.safestring import mark_safe

from report.models import Report


class ReportTable(tables.Table):
    download = tables.Column(orderable=False, verbose_name="", empty_values=())

    type_str = tables.Column(orderable=True, verbose_name="Тип")
    measure = tables.Column(orderable=True, verbose_name="Единица измерения")

    class Meta:
        model = Report
        template_name = "django_tables2/bootstrap.html"
        fields = ('download', 'start_date', 'end_date', 'status')

    def render_download(self, value, record):
        if self.request.user.is_authenticated:
            if record.status == 'OK':
                return 'Заглушка'
            return ''
        return ''
