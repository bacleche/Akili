from django.contrib import admin

from EtudiantApp.data_models.etudiant import Etudiant
from EtudiantApp.data_models.demande import Demande
from EtudiantApp.data_models.memoire import Memoire
from EtudiantApp.data_models.notifications import Notification
from CSSAPP.data_models.css import CSS
from CSSAPP.data_models.documents import Attestation , Bulletin

from DCFISPACE.data_models.directeur import Directeur

from Utilisateur.data_models.utilisateur import Utilisateur


class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name'  ,'telephone', 'email', 'genre')
    search_fields = ('last_name','first_name' ,  'telephone', 'email')
    list_filter = ('genre',)


class EtudiantAdmin(UtilisateurAdmin):
    list_display = ('matricule', 'Identification' , 'cycle', 'filiere', 'niveaux', 'statut' , 'role')
    search_fields = ('matricule', 'Identification' , 'cycle', 'filiere' , 'role')
    list_filter = ('cycle', 'filiere', 'niveaux', 'statut')

admin.site.register(Etudiant, EtudiantAdmin)

class CSSAdmin(UtilisateurAdmin):
    list_display = ('matricule' ,'genre' , 'role')
    search_fields = ('matricule', 'genre'  , 'role')
    list_filter = ('genre', 'role')


admin.site.register(CSS, CSSAdmin)

class DirecteurAdmin(UtilisateurAdmin):
    list_display = ('matricule' ,'genre' , 'role')
    search_fields = ('matricule', 'genre'  , 'role')
    list_filter = ('genre', 'role')

admin.site.register(Directeur, DirecteurAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('destinataire', 'contenu', 'est_lue', 'date_creation')
    search_fields = ('destinataire__nom', 'contenu')
    list_filter = ('est_lue', 'date_creation')

admin.site.register(Notification, NotificationAdmin)




class AttestationAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'types_attestation','is_signed')
    search_fields = ('etudiant', 'types_attestation')
    list_filter = ('is_signed','date_register')

admin.site.register(Attestation, AttestationAdmin)


class BulletinAdmin(admin.ModelAdmin):
    list_display = ('etudiant','is_signed')
    search_fields = ('etudiant', 'date_register')
    list_filter = ('is_signed','date_register')

admin.site.register(Bulletin, BulletinAdmin)


class DemandeAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'objet_demande', 'session_dut', 'session_lic', 'filiere', 'cycle', 'annee_academique', 'identite_receptioniste' , 'etat')
    search_fields = ('etudiant__nom', 'etudiant__prenom', 'objet_demande', 'filiere', 'cycle', 'annee_academique', 'identite_receptioniste__nom', 'identite_receptioniste__prenom')
    list_filter = ('objet_demande', 'filiere', 'cycle', 'annee_academique', 'identite_receptioniste' , 'etat')

admin.site.register(Demande, DemandeAdmin)



class MemoireAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_poste', 'identite', 'matricule_identification_binome', 'binome_notification_envoyee')
    search_fields = ('titre', 'identite__nom', 'identite__prenom', 'matricule_identification_binome')
    list_filter = ('date_poste', 'binome_notification_envoyee')

admin.site.register(Memoire, MemoireAdmin)