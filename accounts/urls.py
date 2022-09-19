from django.urls import path

from .views import SignUpView, EditUserView
from .views import CustomLoginView

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('<int:pk>/edit/', EditUserView.as_view(), name='edit_user'),
]