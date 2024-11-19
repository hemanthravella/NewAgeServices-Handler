
from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('v1/item/<int:item_id>', views.MenuItemDetailView.as_view(), name='menu-item-detail'),
    path('v1/createItem', views.MenuItemsView.as_view(), name='menu-item-create'),
    path('v1/item/<int:item_id>/patch', views.MenuItemsPatchView.as_view(), name='menu-item-patch'),
    path('v1/item/<int:item_id>/delete', views.MenuItemDeleteView.as_view(), name='menu-item-delete'),

]
