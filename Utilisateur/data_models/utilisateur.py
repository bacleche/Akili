from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User

class UtilisateurManager(models.Manager):
    pass


class Role(models.TextChoices):
    CSS = 'CSS', 'CSS'
    DIRECTEUR = 'Directeur', 'Directeur'
    ETUDIANT = 'Etudiant', 'Etudiant'


class Civilite(models.TextChoices):
    MARIE = 'MARIÉ' , 'MARIÉ'
    VEUF = 'VEUF(VE)' , 'VEUF(VE)'
    CELIBATAIRE = 'Célibataire' , 'Célibataire'

class Genre(models.TextChoices):
    HOMME = 'Homme' , 'Homme'
    FEMME = 'Femme' , 'Femme'


class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_login = models.BooleanField(default=True)
    telephone = models.CharField(max_length=255)
    date_nais = models.DateField()
    civilite = models.CharField(max_length=20, choices=Civilite.choices , default=Civilite.CELIBATAIRE)
    genre = models.CharField(max_length=20 , choices=Genre.choices , default=Genre.HOMME)
    imagesprofiles = models.ImageField(upload_to='images/',max_length=500,default='images/r.jpeg') 
    role = models.CharField(max_length=20 , choices=Role.choices)


    objects = UtilisateurManager()
    class Meta:
        abstract = True

    def clean(self):
        """
        Méthode de validation pour s'assurer que l'utilisateur a au moins 18 ans.
        """
        age_minimum = 18
        age_maximum = 120  # Vous pouvez ajuster cette valeur selon vos besoins

        if self.date_nais:
            age = timezone.now().year - self.date_nais.year - ((timezone.now().month, timezone.now().day) < (self.date_nais.month, self.date_nais.day))

            if age < age_minimum or age > age_maximum:
                raise ValidationError({'date_nais': f"Âge invalide. Vous devez avoir entre {age_minimum} et {age_maximum} ans."})

        if len(self.telephone) < 9:
            raise ValidationError({'telephone': "Le numéro de téléphone doit avoir au moins 9 caractères."})
