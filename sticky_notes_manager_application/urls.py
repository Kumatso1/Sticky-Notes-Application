from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/create/', views.create_admin, name='create_admin'),
    path('sticky_notes_manager_application/', views.note_list, name='note_list'),
    path('sticky_notes_manager_application/<int:pk>/', views.note_detail, name='note_detail'),
    path('sticky_notes_manager_application/new/', views.note_new, name='note_new'),
    path('sticky_notes_manager_application/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('sticky_notes_manager_application/<int:pk>/delete/', views.note_delete, name='note_delete'),
]
