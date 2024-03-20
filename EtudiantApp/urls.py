from django.urls import path
from . import views

urlpatterns = [
    path('student_space', views.EtudiantSPACE, name='student_space'),
    path('Profiles_etudiant', views.Profiles_etudiant, name='Profiles_etudiant'),  
    path('profile_details_etudiant', views.profile_details_etudiant, name='profile_details_etudiant'),  
    path('mis_a_jour_etudiant', views.mis_a_jour_etudiant, name='mis_a_jour_etudiant'),  
    path('poster_memoire', views.poster_memoire, name='poster_memoire'),   
    path('creer_demande/', views.creer_demande, name='creer_demande'),  
    path('marquer_notification_lue/<int:notification_id>/', views.marquer_notification_lue, name='marquer_notification_lue'),
    path('creer_nouvelle_notification/', views.creer_nouvelle_notification, name='creer_nouvelle_notification'),
    path('registre_demande' , views.registre_demande, name='registre_demande'),
    path('imprimer_demande/<int:demande_id>/', views.imprimer_demande, name='imprimer_demande'),
    path('supprimer_demande/<int:demande_id>/', views.supprimer_demande, name='supprimer_demande'),
    path('modifier_demande/<int:demande_id>/', views.modifier_demande, name='modifier_demande'),
    path('registre_bulletins', views.registre_bulletins, name='registre_bulletins'),
    path('registre_attestations', views.registre_attestations, name='registre_attestations'),
    # path('archive_documentsbulletins', views.archive_documentsbulletins, name='archive_documentsbulletins'),
    path('recherche_demande_de_etudiant', views.recherche_demande_de_etudiant, name='recherche_demande_de_etudiant'),



]
