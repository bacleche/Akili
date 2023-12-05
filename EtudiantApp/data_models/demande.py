from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from EtudiantApp.data_models.etudiant import Etudiant
from CSSAPP.data_models.css import CSS


class Demande(models.Model):
    OBJET_CHOICES = (
        ('attestation_frequentation', 'Attestation de fréquentation'),
        ('attestation_reussite', 'Attestation de réussite'),
        ('bulletin', 'Bulletin'),
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

    ANNEE_ACADEMIQUE_CHOICES = [
        ('2023 - 2024', '2023 - 2024'),
        ('2024 - 2025', '2024 - 2025'),
        ('2025 - 2026', '2025 - 2026'),
        ('2026 - 2027', '2026 - 2027'),
        ('2027 - 2028', '2027 - 2028'),
        ('2028 - 2029', '2028 - 2029'),
        ('2029 - 2030', '2029 - 2030'),
    ]

    identite_concerne = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    objet_demande = models.CharField(max_length=50, choices=OBJET_CHOICES)
    session_dut = models.CharField(max_length=2, choices=SESSION_CHOICES_DUT)
    session_lic = models.CharField(max_length=2, choices=SESSION_CHOICES_LICENCE)
    filiere = models.CharField(max_length=50, choices=FILIERE_CHOICES)
    cycle = models.CharField(max_length=50, choices=CYCLE_CHOICES)
    annee_academique = models.CharField(max_length=50 , choices=ANNEE_ACADEMIQUE_CHOICES)
    identite_receptioniste = models.ForeignKey(CSS, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        current_year = timezone.now().year

        if int(self.annee_academique.split(' - ')[0]) > current_year:
            raise ValidationError("L'année académique ne peut pas être supérieure à l'année en cours.")
        
        if self.cycle == 'DUT':
            self.session_lic = None  # Si le cycle est DUT, videz le champ session_lic
        elif self.cycle == 'LICENCE':
            self.session_dut = None  # Si le cycle est LICENCE, videz le champ session_dut
        
        super(Demande, self).save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.get_objet_demande_display()} - {self.session_dut or self.session_lic} - {self.filiere} - {self.cycle} - {self.annee_academique}'
