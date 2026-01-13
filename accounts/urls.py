from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),

    # Dashboard
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Admin views
    path('admin_applications/', views.admin_application, name='admin_applications'),
    path('admin_user/', views.admin_user, name='admin_user'),
    path('admin_renewals/', views.admin_renewal, name='admin_renewals'),
    path('admin_archive/', views.admin_archive, name='admin_archive'),

    # Admin Application Actions
    path('admin_application/<int:app_id>/accept/', views.accept_application, name='accept_application'),
    path('admin_application/<int:app_id>/reject/', views.reject_application, name='reject_application'),

    # Admin Renewal Action
    path('admin_renewals/<int:renewal_id>/accept/', views.accept_renewal, name='accept_renewal'),
    path('admin_renewals/<int:renewal_id>/reject/', views.reject_renewal, name='reject_renewal'),

    # Admin User Actions
    path('admin/user/<int:user_id>/ban/', views.ban_user, name='ban_user'),

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
    # path('delete_renewal/<int:renewal_id>/', views.delete_renewal, name='delete_renewal'), # Admin only

    # Crude for Student Profiles
    path('update_profile/', views.update_profile, name='update_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),

    path('documents/', views.user_documents, name='user_documents'),

]
