from django.urls import path
from . import views

urlpatterns = [
    path('student_space', views.EtudiantSPACE, name='student_space'),
    path('Profiles_etudiant', views.Profiles_etudiant, name='Profiles_etudiant'),  
    path('profile_details_etudiant', views.profile_details_etudiant, name='profile_details_etudiant'),  
    path('mis_a_jour_etudiant', views.mis_a_jour_etudiant, name='mis_a_jour_etudiant'),  
    path('poster_memoire', views.poster_memoire, name='poster_memoire'),   
    path('creer_demande', views.creer_demande, name='creer_demande'),  




]