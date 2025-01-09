from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('write/', views.write, name='write'),
    path('person_registration', views.person_registration, name='person_registration'),
    path('day/', views.day, name='day'),
    path('remove_day/', views.remove_day, name='remove_day'),
]
