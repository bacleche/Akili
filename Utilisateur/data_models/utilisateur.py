from django.db import models

from django.contrib.auth.models import User

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
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
    date_nais = models.DateField()
    civilite = models.CharField(max_length=20, choices=Civilite.choices , default=Civilite.CELIBATAIRE)
    email = models.EmailField(unique=True , default=None)
    genre = models.CharField(max_length=20 , choices=Genre.choices , default=Genre.HOMME)
    imagesprofiles = models.ImageField(upload_to='images/',max_length=500,default='images/r.jpeg') 

    class Meta:
        abstract = True
