from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.apply_scholarship, name='apply_scholarship'),
    path('review/', views.review_applications, name='review_applications'),

    # renewal
    path('renewal/apply/', views.apply_renewal, name='apply_renewal'),

]
