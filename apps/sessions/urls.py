from django.urls import path

from . import views

urlpatterns = [
    path('', views.SessionsList.as_view(), name='sessions'),
    path('create/', views.CreateSessionWithPresences.as_view(), name='create_session'),
    path('<int:pk>/', views.DetailSession.as_view(), name='detail_session'),
    path('<int:pk>/edit/', views.UpdateSession.as_view(), name='edit_session'),
    path('<int:pk>/validate/', views.validate_session, name='validate_session'),
    path('<int:pk>/delete/', views.DeleteSession.as_view(), name='delete_session'),
    path('<int:pk>/duplicate/', views.duplicate_session, name='duplicate_session'),
    path('create/<int:student_id>/', views.update_product_when_selecting_student,
         name='update-product-when-selecting-student'),
    path('<int:pk>/print-presences/', views.print_presences, name='print-presences')
]
