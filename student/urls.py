from django.urls import path
from . import views


urlpatterns = [
    path('', views.student_index, name="student_index"),
    path('signIn', views.student_signIn, name="student_signIn"),
    path('logIn', views.student_logIn, name="student_logIn"),
    path('dashboard', views.student_dashboard, name="student_dashboard"),
    path('logout', views.student_logout, name="student_logout"),
    path('success', views.student_register_success, name="student_register_success"),
]