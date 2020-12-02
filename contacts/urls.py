from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='contacts'),
    path('<int:contact_id>/', views.contact_detail, name='contact_detail'),
]