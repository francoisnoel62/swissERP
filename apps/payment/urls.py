from django.urls import path

from . import views

urlpatterns = [
    path('', views.PaymentListView.as_view(), name='payments'),
    path('', views.PaymentCreateView.as_view(), name='create_payment'),
]