from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from EtudiantApp.data_models.etudiant import Etudiant
from CSSAPP.data_models.css import CSS


class Demande(models.Model):
    OBJET_CHOICES = (
        ('attestation_frequentation', 'Attestation de fréquentation'),
        ('attestation_reussite', 'Attestation de réussite'),
        ('releve', 'Relevé'),
    )
    
    SESSION_CHOICES_DUT = (
        ('S1', 'S1'),
        ('S2', 'S2'),
        ('S3', 'S3'),
        ('S4', 'S4'),
    )
    
    SESSION_CHOICES_LICENCE = (
        ('S1', 'S1'),
        ('S2', 'S2'),
        ('S3', 'S3'),
        ('S4', 'S4'),
        ('S5', 'S5'),
        ('S6', 'S6'),
    )
    
    FILIERE_CHOICES = (
        ('informatique', 'Informatique'),
        ('administration', 'Administration'),
    )
    
    CYCLE_CHOICES = (
        ('DUT', 'DUT'),
        ('LICENCE', 'Licence'),
    )

    identite_concerne = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    objet_demande = models.CharField(max_length=50, choices=OBJET_CHOICES)
    session = models.CharField(max_length=2, choices=SESSION_CHOICES_DUT)
    filiere = models.CharField(max_length=50, choices=FILIERE_CHOICES)
    cycle = models.CharField(max_length=50, choices=CYCLE_CHOICES)
    annee_academique = models.CharField(max_length=10)
    identite_receptioniste = models.ForeignKey(CSS, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        current_year = timezone.now().year

        if int(self.annee_academique) > current_year:
            raise ValidationError("L'année académique ne peut pas être supérieure à l'année en cours.")
        
        if self.cycle == 'LICENCE':
            self.session = self.session if self.session in [s[0] for s in self.SESSION_CHOICES_LICENCE] else 'S1'
        else:
            self.session = self.session if self.session in [s[0] for s in self.SESSION_CHOICES_DUT] else 'S1'
        
        super(Demande, self).save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.get_objet_demande_display()} - {self.session} - {self.filiere} - {self.cycle} - {self.annee_academique}'
