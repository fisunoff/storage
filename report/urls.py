from django.urls import path

from report.views import ReportCreateView, ReportListView

urlpatterns = [
    path('', ReportListView.as_view(), name='report-list'),
    path('create/', ReportCreateView.as_view(), name='report-create'),
    # path('<int:pk>/', OperationDetailView.as_view(), name='report-detail'),
    # path('<int:pk>/update/', OperationUpdateView.as_view(), name='report-update'),
]
