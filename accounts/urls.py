from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),


    # Dashboard
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Settings
    path('student/settings/', views.student_settings, name='student_settings'),

    # Forms
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('apply/', views.apply_scholarship, name='apply_scholarship'),
    path('renewal/apply/', views.apply_renewal, name='apply_renewal'),

    # Crude for Admin
    path('delete/<int:app_id>/', views.delete_application, name='delete_application'), # Admin only
    path('delete_renewal/<int:renewal_id>/', views.delete_renewal, name='delete_renewal'), # Admin only

    # Crude for Student Profiles
    path('update_profile/', views.update_profile, name='update_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),


]
