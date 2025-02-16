
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('v1/orders/<int:order_id>', views.OrderDetailView.as_view(), name='order-detail'),
    path('v1/orders/create', views.CreateOrderView.as_view(), name='create-order'),
]
