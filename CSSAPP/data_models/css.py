from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from Utilisateur.data_models.utilisateur import Utilisateur




class CSS(Utilisateur):
    # Vos autres champs

    matricule = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=255)
    confirmer_mot_de_passe = models.CharField(max_length=255)

    def clean(self):
        # Assurez-vous que les mots de passe ont au moins 8 caractères
        if len(self.mot_de_passe) < 8:
            raise ValidationError("Le mot de passe doit comporter au moins 8 caractères.")
        if len(self.confirmer_mot_de_passe) < 8:
            raise ValidationError("La confirmation du mot de passe doit comporter au moins 8 caractères.")
        
        # Vérifiez que les deux champs de mot de passe sont identiques
        if self.mot_de_passe != self.confirmer_mot_de_passe:
            raise ValidationError("Les mots de passe ne correspondent pas.")

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


@receiver(pre_save, sender=CSS)
def css_pre_save(sender, instance, **kwargs):
    if not instance.matricule:
        instance.matricule = instance.generate_matricule()
