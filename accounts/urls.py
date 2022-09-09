from django.urls import path

from .views import SignUpView

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    # path('<int:pk>/edit/', views.EditUser.as_view(), name='edit_user'),
    # path('change_password/', views.change_pass, name='change_pass'),
    # path('reset_password/', views.reset_password, name='reset_password'),
    # path('password-reset-confirm/<uidb64>/<token>',
    #      auth_view.PasswordResetConfirmView.as_view(),
    #      name="password_reset_confirm"),
    # path('password_reset_complete/',
    #      views.PasswordResetCompleteViewInherit.as_view(),
    #      name="password_reset_complete"),
]