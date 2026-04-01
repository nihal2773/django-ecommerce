from django.urls import path
from .views import OrderHistoryView, CreateOrderView, PaymentView

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create-order'),
    path('history/', OrderHistoryView.as_view(), name='order-history'),
    path('pay/<int:order_id>/', PaymentView.as_view()), 
]