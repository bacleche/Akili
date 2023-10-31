from django.urls import path
from . import views

urlpatterns = [
    path('student_space', views.EtudiantSPACE, name='student_space'),
]