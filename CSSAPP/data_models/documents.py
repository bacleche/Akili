from django.db import models
from EtudiantApp.data_models.etudiant import Etudiant
from DCFISPACE.data_models.directeur import Directeur
from CSSAPP.data_models.css import CSS
from EtudiantApp.data_models.notifications import Notification

from django.dispatch import receiver
from django.db.models.signals import post_save

class Attestation(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.DO_NOTHING)
    types_attestation = models.CharField(max_length=500)
    date_register = models.DateField(auto_now_add=True)
    is_signed = models.BooleanField(default=False)
    is_transfer_directeur = models.BooleanField(default=False)
    is_transfer_css = models.BooleanField(default=False)
    is_transfer_etudiant = models.BooleanField(default=False)
    file = models.ImageField(upload_to='attestations/',max_length=500) 
    profile_directeur = models.ForeignKey(Directeur , on_delete=models.DO_NOTHING , default=1)
    profiles_css = models.ForeignKey(CSS , on_delete=models.DO_NOTHING , default=1)
    is_archived = models.BooleanField(default=False)

    
    def __str__(self):
        return f"Attestation de {self.etudiant.user.first_name} {self.etudiant.user.last_name}"



@receiver(post_save, sender=Attestation)
def create_attestation_notification(sender, instance, created, **kwargs):
    if created:
        # Créer la notification pour l'attestation
        destinataire_directeur = instance.profile_directeur
        expediteur_css = instance.profiles_css
        contenu_notification = f"L'attestation de {instance.etudiant.user.first_name} {instance.etudiant.user.last_name} a été créée."
        date_creation = instance.date_register

        notification = Notification.objects.create(
            destinataire_dir=destinataire_directeur,
            expediteur_css=expediteur_css,
            contenu=contenu_notification,
            date_creation=date_creation
        )
        notification.save()
        print('notif marché')


class Bulletin(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.DO_NOTHING)
    date_register = models.DateField(auto_now_add=True)
    is_signed = models.BooleanField(default=False)  
    is_transfer_directeur = models.BooleanField(default=False)
    is_transfer_css = models.BooleanField(default=False)
    is_transfer_etudiant = models.BooleanField(default=False)
    file = models.ImageField(upload_to='bulletins/',max_length=500) 
    profile_directeur = models.ForeignKey(Directeur , on_delete=models.DO_NOTHING, default=1)
    profiles_css = models.ForeignKey(CSS , on_delete=models.DO_NOTHING, default=1)
    is_archived = models.BooleanField(default=False)
 
    def __str__(self):
        return f"Bulletin de {self.etudiant.user.first_name} {self.etudiant.user.last_name}"

@receiver(post_save, sender=Bulletin)
def create_bulletin_notification(sender, instance, created, **kwargs):
    if created:
        # Créer la notification pour le bulletin
        destinataire_directeur = instance.profile_directeur
        expediteur_css = instance.profiles_css
        contenu_notification = f"Le bulletin de {instance.etudiant.user.first_name} {instance.etudiant.user.last_name} a été créé."
        date_creation = instance.date_register

        notification = Notification.objects.create(
            destinataire_dir=destinataire_directeur,
            expediteur_css=expediteur_css,
            contenu=contenu_notification,
            date_creation=date_creation
        )
        notification.save()
        print('notif bulletin')

