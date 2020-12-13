from django.urls import path

from . import views

urlpatterns = [
    path('branch', views.branch, name="branch"),
    path('item', views.item, name="item"),
    path('transaction', views.transaction, name="transaction"),
    path('inventory', views.inventory, name="inventory"),
    
]

