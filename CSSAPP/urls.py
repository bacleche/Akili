from django.urls import path
from . import views
from . import creationsdocuments

urlpatterns = [
    path('css_space', views.cssWork, name='cssWork'),
    path('Profiles_css' , views.Profiles_css , name='Profiles_css'),
    path('update_profile' , views.profile_details , name='update_profile'),
    path('mis_a_jour_css' , views.mis_a_jour_css , name='mis_a_jour_css'), 
    path('list_demandes' , views.list_demandes , name='list_demandes'), 
    path('list_bulletin_demandes' , views.list_bulletin_demandes , name='list_bulletin_demandes'), 
    path('imprimer_demande_css/<int:demande_id>/', views.imprimer_demande_css, name='imprimer_demande_css'),
    path('generer_fichier_csv/<int:demande_id>/', views.generer_fichier_csv, name='generer_fichier_csv'),
    path('recherche_demande_par_etudiant/', views.recherche_demande_par_etudiant, name='recherche_demande_par_etudiant'),
    path('recherche_demande_par_etudiant_attestations/', views.recherche_demande_par_etudiant_attestations, name='recherche_demande_par_etudiant_attestations'),
    path('liste_etudiant_classifications' , views.liste_etudiant_classifications , name='liste_etudiant_classifications'),
    path('liste_etudiants_licence' , views.liste_etudiants_licence , name='liste_etudiants_licence'),
    path('supprimer_demande_css_bulletin/<int:demande_id>/' , views.supprimer_demande_css_bulletin , name='supprimer_demande_css_bulletin'),
    path('supprimer_demande_css_attestation/<int:demande_id>/' , views.supprimer_demande_css_attestation , name='supprimer_demande_css_attestation'),
    path('liste_etudiants_licence_info2' , views.liste_etudiants_licence_info2 , name='liste_etudiants_licence_info2'),
    path('liste_etudiants_licence_info3' , views.liste_etudiants_licence_info3 , name='liste_etudiants_licence_info3'),
    path('liste_etudiants_dut_info1' , views.liste_etudiants_dut_info1 , name='liste_etudiants_dut_info1'),
    path('liste_etudiants_dut_info2' , views.liste_etudiants_dut_info2 , name='liste_etudiants_dut_info2'),
    path('liste_etudiants_administration_dut1' , views.liste_etudiants_administration_dut1 , name='liste_etudiants_administration_dut1'),
    path('liste_etudiants_administration_dut2' , views.liste_etudiants_administration_dut2 , name='liste_etudiants_administration_dut2'),
    path('liste_etudiants_licence_admin1' , views.liste_etudiants_licence_admin1 , name='liste_etudiants_licence_admin1'),
    path('liste_etudiants_licence_admin2' , views.liste_etudiants_licence_admin2 , name='liste_etudiants_licence_admin2'),
    path('liste_etudiants_licence_admin3' , views.liste_etudiants_licence_admin3 , name='liste_etudiants_licence_admin3'),
    path('changer_etat_demande_bulletin/<int:demande_id>/<str:action>/', views.changer_etat_demande_bulletin, name='changer_etat_demande_bulletin'),
    path('changer_etat_demande_attestion/<int:demande_id>/<str:action>/', views.changer_etat_demande_attestion, name='changer_etat_demande_attestion'),
    path('update_etudiant_statut/<str:etudiant_id>/', views.update_etudiant_statut, name='update_etudiant_statut'),
    path('historique_demandes/', views.historique_demandes, name='historique_demandes'),
    path('stat_morris/', views.stat_morris, name='stat_morris'),
    path('taux_etudiants/', views.taux_etudiants, name='taux_etudiants'),
    # URLS DE CREATION DE DOCUMENT POUR TOUTES LES CLASSES !!! 
    path('create_document/<int:etudiant_id>', creationsdocuments.create_document_lic1_info, name='create_document'),
    path('create_document_lic2_info/<int:etudiant_id>', creationsdocuments.create_document_lic2_info, name='create_document_lic2_info'),
    path('create_document_lic3_info/<int:etudiant_id>', creationsdocuments.create_document_lic3_info, name='create_document_lic3_info'),
    path('create_document_lic1_admin/<int:etudiant_id>', creationsdocuments.create_document_lic1_admin, name='create_document_lic1_admin'),
    path('create_document_lic2_admin/<int:etudiant_id>', creationsdocuments.create_document_lic2_admin, name='create_document_lic2_admin'),
    path('create_document_lic3_admin/<int:etudiant_id>', creationsdocuments.create_document_lic3_admin, name='create_document_lic3_admin'),
    path('create_document_dut1_admin/<int:etudiant_id>', creationsdocuments.create_document_dut1_admin, name='create_document_dut1_admin'),
    path('create_document_dut2_admin/<int:etudiant_id>', creationsdocuments.create_document_dut2_admin, name='create_document_dut2_admin'),
    path('create_document_dut1_info/<int:etudiant_id>', creationsdocuments.create_document_dut1_info, name='create_document_dut1_info'),
    path('create_document_dut2_info/<int:etudiant_id>', creationsdocuments.create_document_dut2_info, name='create_document_dut2_info'),
    path('liste_Attestations', views.liste_Attestations, name='liste_Attestations'),
    path('liste_bulletinsf', views.liste_bulletinsf, name='liste_bulletinsf'),
    path('recherche_attestation_css', views.recherche_attestation_css, name='recherche_attestation_css'),
    path('recherche_Bulletins_css', views.recherche_Bulletins_css, name='recherche_Bulletins_css'),
    path('signaler_css_bulletin_etudiant/<int:bulletin_id>', views.signaler_css_bulletin_etudiant, name='signaler_css_bulletin_etudiant'),
    path('signaler_css_attestation_etudiant/<int:attestation_id>', views.signaler_css_attestation_etudiant, name='signaler_css_attestation_etudiant'),
    path('imprimer_attestation_css_doc', views.imprimer_attestations_css_doc, name='imprimer_attestation_css_doc'),
    path('imprimer_bulletin_css_doc', views.imprimer_bulletins_css_doc, name='imprimer_bulletin_css_doc'),





    #EN BAS UR DE DECONNEXION
    path('deconnexion' , views.custom_logout , name='deconnexion'),


]    
