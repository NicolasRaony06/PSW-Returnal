from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('write/', views.write, name='write'),
    path('person_registration', views.person_registration, name='person_registration'),
]
