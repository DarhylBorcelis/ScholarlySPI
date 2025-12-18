from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),


    # dashboard
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # forms
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # crude
    path('update/<int:app_id>/', views.update_application_status, name='update_application'),
    path('delete/<int:app_id>/', views.delete_application, name='delete_application'),
    path('update_renewal/<int:renewal_id>/', views.update_renewal_status, name='update_renewal'),
    path('delete_renewal/<int:renewal_id>/', views.delete_renewal, name='delete_renewal'),


]
