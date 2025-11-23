from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard', views.student_dashboard, name="student_dashboard"),
    path('signIn', views.student_signIn, name="student_signIn"),
]