from django.urls import path
from . import views


urlpatterns = [
    path('', views.student_index, name="student_index"),
    path('signUp', views.student_signUp, name="student_signUp"),
    path('logIn', views.student_logIn, name="student_logIn"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('logout', views.student_logout, name="student_logout"),
    path('success', views.student_register_success, name="student_register_success"),
]