from django.urls import path

from . import views

urlpatterns = [
    path('branch', views.branch, name="branch"),
    path('item', views.item, name="item"),
    path('transaction', views.transaction, name="transaction"),
    path('inventory', views.inventory, name="inventory"),
    path('distributiontocontractors', views.distributiontocontractors, name="distributiontocontractors"),
    path('billing', views.billing, name="billing"),
    path('contractorinfo', views.contractorinfo, name="contractorinfo"),
    
]

