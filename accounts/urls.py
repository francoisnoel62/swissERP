from django.urls import path

from .views import SignUpView
from .views import CustomLoginView

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
]