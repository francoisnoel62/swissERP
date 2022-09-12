from django.urls import path

from . import views

urlpatterns = [
    path('', views.SaleOrderIndexView.as_view(), name='sales'),
    path('', views.SaleOrderIndexView.as_view(), name='filter_sales'),
    path('create/', views.SaleOrderCreateViewWithSOL.as_view(), name='create_sale'),
    path('<int:pk>/edit', views.SaleOrderUpdateViewWithSOL.as_view(), name='edit_sale'),
    path('<int:pk>/', views.SaleOrderView.as_view(), name='sale_detail'),
    path('<int:pk>/delete', views.SaleOrderDeleteView.as_view(), name='delete_sale'),
    path('<int:order_id>/confirm', views.confirm_order, name='confirm_sale'),
    path('<int:order_id>/generate_pdf/', views.generate_pdf, name='generate_pdf'),
]