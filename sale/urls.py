from django.urls import path

from . import views

urlpatterns = [
    path('', views.SaleOrderIndexView.as_view(), name='sales'),
    path('create/', views.SaleOrderCreateView.as_view(), name='create_sale'),
    path('create-line/', views.SaleOrderLineCreateView.as_view(), name='create_sale_order'),
    path('<int:pk>/edit/', views.EditSOLView.as_view(), name='edit_sol'),
]