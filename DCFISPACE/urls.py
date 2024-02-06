from django.urls import path
from . import views

urlpatterns = [
    path('Home_Directeur', views.Home_Directeur, name='Home_Directeur'),

]