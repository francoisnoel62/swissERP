from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='products'),
    path('', views.ProductListView.as_view(), name='filter_products'),
    path('create_pass', views.ProductCreatePassView.as_view(), name='create-pass'),
    path('create_subscription', views.ProductCreateSubView.as_view(), name='create-subscription'),
    path('<int:pk>/edit', views.ProductUpdateView.as_view(), name='edit-product'),
    path('<int:pk>/delete', views.ProductDeleteView.as_view(), name='delete-product')
]
