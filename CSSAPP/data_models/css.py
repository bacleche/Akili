from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from Utilisateur.data_models.utilisateur import Utilisateur , UtilisateurManager


class CSSManager(UtilisateurManager):
    pass



class CSS(Utilisateur):

    matricule = models.CharField(max_length=20, unique=True, blank=True, editable=False)

    objects = CSSManager()

    def save(self, *args, **kwargs):
        if not self.matricule:
            self.matricule = self.generate_matricule()
        self.clean() 

        super(CSS, self).save(*args, **kwargs)

    def generate_matricule(self):
        last_css = CSS.objects.order_by('-matricule').first()
        if last_css:
            last_matricule = last_css.matricule
            matricule_number = int(last_matricule[1:]) + 1
        else:
            matricule_number = 1
        return f'C{matricule_number:06d}'
    
    def __str__(self):
          return f"{self.user.last_name} {self.user.first_name}"


@receiver(pre_save, sender=CSS)
def css_pre_save(sender, instance, **kwargs):
    if not instance.matricule:
        instance.matricule = instance.generate_matricule()



#Ceci est le profil du CHef de service de la Scolarité