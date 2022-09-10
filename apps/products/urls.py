from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='products'),
    path('create', views.ProductCreateView.as_view(), name='create-product'),
    path('<int:pk>/edit', views.ProductUpdateView.as_view(), name='edit-product'),
    path('<int:pk>/delete', views.ProductDeleteView.as_view(), name='delete-product')
]
