from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='products'),
    path('edit', views.ProductCreateView.as_view(), name='create-product')
]
