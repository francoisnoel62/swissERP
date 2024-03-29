from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='contacts'),
    path('', views.IndexView.as_view(), name='filter_contacts'),
    path('<int:contact_id>', views.toggle_active, name='toggle_active'),
    path('create/', views.CreateView.as_view(), name='create_contact'),
    path('<int:pk>/edit/', views.EditView.as_view(), name='edit_contact'),
    path('<int:pk>/', views.DetailView.as_view(), name='contact_detail'),
    path('<int:pk>/delete/', views.DeleteView.as_view(), name='delete_contact'),
    path('import/', views.upload_file, name='import_contacts'),
]