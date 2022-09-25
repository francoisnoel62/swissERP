from django.urls import path

from . import views

urlpatterns = [
    path('', views.SessionsList.as_view(), name='sessions'),
    path('create/', views.CreateSession.as_view(), name='create_session'),
]