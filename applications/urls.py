from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.apply_scholarship, name='apply_scholarship'),
    path('my-applications/', views.student_applications, name='student_applications'),
    path('review/', views.review_applications, name='review_applications'),
]
