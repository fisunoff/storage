from django.urls import path

from stock.views import StockCreateView, StockDetailView, StockUpdateView, StockListView

urlpatterns = [
    path('', StockListView.as_view(), name='stock-list'),
    path('create/', StockCreateView.as_view(), name='stock-create'),
    path('<int:pk>/', StockDetailView.as_view(), name='stock-detail'),
    path('<int:pk>/update/', StockUpdateView.as_view(), name='stock-update'),
]
