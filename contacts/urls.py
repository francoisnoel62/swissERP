from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='contacts'),
    path('create/', views.CreateView.as_view(), name='create_contact'),
    path('<int:pk>/', views.DetailView.as_view(), name='contact_detail')
]