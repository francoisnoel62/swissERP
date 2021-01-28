from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='contacts'),
    path('<int:contact_id>/', views.detail, name='contact_detail'),
]