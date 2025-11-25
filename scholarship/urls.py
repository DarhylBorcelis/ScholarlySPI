from django.urls import path
from . import views


urlpatterns = [
    path('', views.scholarship_index, name='scholarship_index')
]