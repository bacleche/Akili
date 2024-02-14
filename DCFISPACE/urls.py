from django.urls import path
from . import views

urlpatterns = [
    path('Home_Directeur', views.Home_Directeur, name='Home_Directeur'),
    path('Profiles_directeur', views.Profiles_directeur  , name='Profiles_directeur'),
    path('profile_details_directeur', views.profile_details_directeur  , name='profile_details_directeur'),
    path('mis_a_jour_directeur', views.mis_a_jour_directeur  , name='mis_a_jour_directeur'),
    path('liste_Attestations_directeur', views.liste_Attestations_directeur  , name='liste_Attestations_directeur'),
    path('liste_Bulletins_directeur', views.liste_Bulletins_directeur  , name='liste_Bulletins_directeur'),
    path('signer_attestation/<int:attestation_id>', views.signer_attestation, name='signer_attestation'),
    path('recherche_Attestations_directeur', views.recherche_Attestations_directeur, name='recherche_Attestations_directeur'),
    path('recherche_Bulletins_directeur', views.recherche_Bulletins_directeur, name='recherche_Bulletins_directeur'),
    path('signaler_css_attestation_directeur/<int:attestation_id>', views.signaler_css_attestation_directeur, name='signaler_css_attestation_directeur'),
    path('imprimer_attestations_directeur', views.imprimer_attestations_directeur, name='imprimer_attestations_directeur'),


]