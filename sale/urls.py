from django.urls import path

from . import views

urlpatterns = [
    path('', views.SaleOrderIndexView.as_view(), name='sales'),
    path('create/', views.SaleOrderCreateView.as_view(), name='create_sale'),
    path('<int:pk>/edit', views.SaleOrderUpdateView.as_view(), name='edit_sale'),
    path('<int:pk>/', views.SaleOrderDetailView.as_view(), name='sale_detail'),
]