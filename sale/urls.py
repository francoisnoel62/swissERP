from django.urls import path

from . import views

urlpatterns = [
    path('', views.SaleOrderIndexView.as_view(), name='sales'),
    path('create/', views.SaleOrderCreateView.as_view(), name='create_sale'),
]