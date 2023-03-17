from django.urls import path

from . import views
from .views import validate_session

urlpatterns = [
    path('', views.SessionsList.as_view(), name='sessions'),
    path('create/', views.CreateSession.as_view(), name='create_session'),
    path('<int:pk>/', views.DetailSession.as_view(), name='detail_session'),
    path('sessions/<int:pk>/edit/', views.UpdateSession.as_view(), name='edit_session'),
    path('sessions/<int:pk>/validate/', validate_session, name='validate_session')
]
