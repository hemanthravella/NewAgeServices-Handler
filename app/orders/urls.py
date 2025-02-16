
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('v1/item/<int:item_id>', views.OrderDetailView.as_view(), name='order-detail'),
]
