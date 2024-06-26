from django.urls import path
from . import views
from . import creationsdocuments
from . import impression_specialise


#URLS POUR L'APP CSS

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
    path('archive_documents_attestation', views.archive_documents_attestation, name='archive_documents_attestation'),
    path('archive_documents_bulletins', views.archive_documents_bulletins, name='archive_documents_bulletins'),
    path('supprimer_bulletin_css', views.supprimer_bulletin_css, name='supprimer_bulletin_css'),
    path('supprimer_attestation_css', views.supprimer_attestation_css, name='supprimer_attestation_css'),
    path('generer_toutes_demandes_csv', views.generer_toutes_demandes_csv, name='generer_toutes_demandes_csv'),
    path('generer_toutes_demandes_csv_bulletins', views.generer_toutes_demandes_csv_bulletins, name='generer_toutes_demandes_csv_bulletins'),
    path('supprimer_demandes_attestation_sup', views.supprimer_demandes_attestation_sup, name='supprimer_demandes_attestation_sup'),
    path('confirmer_suppression_demandes_attestation', views.confirmer_suppression_demandes_attestation, name='confirmer_suppression_demandes_attestation'),
    path('supprimer_demandes_bulletin_sup', views.supprimer_demandes_bulletin_sup, name='supprimer_demandes_bulletin_sup'),
    path('confirmer_suppression_demandes_bulletin', views.confirmer_suppression_demandes_bulletin, name='confirmer_suppression_demandes_bulletin'),
    path('imprimer_toutes_les_demandes_bulletin', views.imprimer_toutes_les_demandes_bulletin, name='imprimer_toutes_les_demandes_bulletin'),
    path('imprimer_toutes_les_demandes_attestations_dem', views.imprimer_toutes_les_demandes_attestations_dem, name='imprimer_toutes_les_demandes_attestations_dem'),
    path('imprimer_etudiant_lic1', impression_specialise.imprimer_etudiant_lic1, name='imprimer_etudiant_lic1'),
    path('imprimer_etudiant_lic2', impression_specialise.imprimer_etudiant_lic2, name='imprimer_etudiant_lic2'),
    path('imprimer_etudiant_lic3', impression_specialise.imprimer_etudiant_lic3, name='imprimer_etudiant_lic3'),
    path('imprimer_etudiant_admin1', impression_specialise.imprimer_etudiant_admin1, name='imprimer_etudiant_admin1'),
    path('imprimer_etudiant_admin2', impression_specialise.imprimer_etudiant_admin2, name='imprimer_etudiant_admin2'),
    path('imprimer_etudiant_admin3', impression_specialise.imprimer_etudiant_admin3, name='imprimer_etudiant_admin3'),
    path('imprimer_etudiant_dut_admin1', impression_specialise.imprimer_etudiant_dut_admin1, name='imprimer_etudiant_dut_admin1'),
    path('imprimer_etudiant_dut_admin2', impression_specialise.imprimer_etudiant_dut_admin2, name='imprimer_etudiant_dut_admin2'),

    path('imprimer_etudiant_dut_informatique1', impression_specialise.imprimer_etudiant_dut_informatique1, name='imprimer_etudiant_dut_informatique1'),
    path('imprimer_etudiant_dut_informatique2', impression_specialise.imprimer_etudiant_dut_informatique2, name='imprimer_etudiant_dut_informatique2'),

    path('listes_anciens_lic_info' , views.listes_anciens_lic_info , name='listes_anciens_lic_info'),
    path('listes_anciens_lic_ap' , views.listes_anciens_lic_ap , name='listes_anciens_lic_ap'),
    path('listes_anciens_dut_info' , views.listes_anciens_dut_info , name='listes_anciens_dut_info'),
    path('listes_anciens_dut_ap' , views.listes_anciens_dut_ap , name='listes_anciens_dut_ap'),


     path('imprimer_etudiant_par_annee/<str:annee_academique>/', views.imprimer_etudiant_par_annee, name='imprimer_etudiant_par_annee'),
    path('update_etudiant_position_soutenance/<str:etudiant_id>/' , views.update_etudiant_position_soutenance , name='update_etudiant_position_soutenance'),


    



    #EN BAS UR DE DECONNEXION
    path('deconnexion' , views.custom_logout , name='deconnexion'),


]    
