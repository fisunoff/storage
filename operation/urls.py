from django.urls import path

from operation.views import OperationCreateView, OperationDetailView, OperationUpdateView, OperationListView

urlpatterns = [
    path('', OperationListView.as_view(), name='operation-list'),
    path('create/', OperationCreateView.as_view(), name='operation-create'),
    path('<int:pk>/', OperationDetailView.as_view(), name='operation-detail'),
    path('<int:pk>/update/', OperationUpdateView.as_view(), name='operation-update'),
]
