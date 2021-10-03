from django.urls import path

from . import views

urlpatterns = [
    path('', views.landingPage, name='landing'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('<int:pk>/edit/', views.EditUser.as_view(), name='edit_user'),
]