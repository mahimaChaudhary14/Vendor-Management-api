"""
URL configuration for vendormanagemenet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# urls.py

from django.urls import path
from vendorapp.views import (
    VendorListCreateView, VendorDetailView,
    PurchaseOrderListCreateView, PurchaseOrderDetailView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/vendors/', VendorListCreateView.as_view(), name='vendor-list'),
    path('api/vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor-detail'),
    path('api/purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase-order-list'),
    path('api/purchase_orders/<int:pk>/', PurchaseOrderDetailView.as_view(), name='purchase-order-detail'),
]



