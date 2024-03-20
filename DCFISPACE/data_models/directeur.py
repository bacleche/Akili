from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from Utilisateur.data_models.utilisateur import Utilisateur , UtilisateurManager


class DirecteurManager(UtilisateurManager):
    pass



class Directeur(Utilisateur):

    matricule = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    signature = models.ImageField(upload_to='signatures/',max_length=500,default='signature/X000001_signature.jpng') 


    objects = DirecteurManager()

    def save(self, *args, **kwargs):
        if not self.matricule:
            self.matricule = self.generate_matricule()
        self.clean() 

        super(Directeur, self).save(*args, **kwargs)

    def generate_matricule(self):
        last_dir = Directeur.objects.order_by('-matricule').first()
        if last_dir:
            last_matricule = last_dir.matricule
            matricule_number = int(last_matricule[1:]) + 1
        else:
            matricule_number = 1
        return f'X{matricule_number:06d}'
    
    def __str__(self):
          return f"{self.user.last_name} {self.user.first_name}"


@receiver(pre_save, sender=Directeur)
def directeur_pre_save(sender, instance, **kwargs):
    if not instance.matricule:
        instance.matricule = instance.generate_matricule()


def signature_filename(instance, filename):
    return f'signatures/{instance.matricule}_signature.png'
@receiver(pre_save, sender=Directeur)
def update_signature_filename(sender, instance, **kwargs):
    instance.signature.name = signature_filename(instance, instance.signature.name)
