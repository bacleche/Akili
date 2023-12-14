from django.db import models

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

