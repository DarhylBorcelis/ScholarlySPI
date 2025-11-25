from django.urls import path
from . import views


urlpatterns = [
    path('', views.student_index, name="index"),
    path('signIn', views.student_signIn, name="student_signIn"),
    path('success', views.student_register_success, name="student_register_success"),
]