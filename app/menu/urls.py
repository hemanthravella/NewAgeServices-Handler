
from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('v1/item/<int:id>', views.MenuItemsDetailsView.as_view(), name='menu-item-detail'),
]
