from django.contrib import admin

from EtudiantApp.data_models.etudiant import Etudiant
from EtudiantApp.data_models.demande import Demande
from EtudiantApp.data_models.memoire import Memoire
from EtudiantApp.data_models.notifications import Notification
from CSSAPP.data_models.css import CSS
from Utilisateur.data_models.utilisateur import Utilisateur


class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'telephone', 'email', 'genre')
    search_fields = ('nom', 'prenom', 'telephone', 'email')
    list_filter = ('genre',)

admin.site.register(Utilisateur, UtilisateurAdmin)

class EtudiantAdmin(UtilisateurAdmin):
    list_display = ('nom', 'prenom', 'matricule', 'Identification' , 'cycle', 'filiere', 'niveaux', 'statut')
    search_fields = ('nom', 'prenom', 'matricule', 'Identification' , 'cycle', 'filiere')
    list_filter = ('cycle', 'filiere', 'niveaux', 'statut')

admin.site.register(Etudiant, EtudiantAdmin)

class CSSAdmin(UtilisateurAdmin):
    list_display = ('nom', 'prenom', 'matricule', 'email')
    search_fields = ('nom', 'prenom', 'matricule', 'email')
    list_filter = ('genre',)


admin.site.register(CSS, CSSAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('destinataire', 'contenu', 'est_lue', 'date_creation')
    search_fields = ('destinataire__nom', 'contenu')
    list_filter = ('est_lue', 'date_creation')

admin.site.register(Notification, NotificationAdmin)


class DemandeAdmin(admin.ModelAdmin):
    list_display = ('identite_concerne', 'objet_demande', 'session_dut', 'session_lic', 'filiere', 'cycle', 'annee_academique', 'identite_receptioniste')
    search_fields = ('identite_concerne__nom', 'identite_concerne__prenom', 'objet_demande', 'filiere', 'cycle', 'annee_academique', 'identite_receptioniste__nom', 'identite_receptioniste__prenom')
    list_filter = ('objet_demande', 'filiere', 'cycle', 'annee_academique', 'identite_receptioniste')

admin.site.register(Demande, DemandeAdmin)



class MemoireAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_poste', 'identite', 'matricule_identification_binome', 'binome_notification_envoyee')
    search_fields = ('titre', 'identite__nom', 'identite__prenom', 'matricule_identification_binome')
    list_filter = ('date_poste', 'binome_notification_envoyee')

admin.site.register(Memoire, MemoireAdmin)