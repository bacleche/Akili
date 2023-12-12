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

    ANNEE_ACADEMIQUE_CHOICES = [
        ('2023 - 2024', '2023 - 2024'),
        ('2024 - 2025', '2024 - 2025'),
        ('2025 - 2026', '2025 - 2026'),
        ('2026 - 2027', '2026 - 2027'),
        ('2027 - 2028', '2027 - 2028'),
        ('2028 - 2029', '2028 - 2029'),
        ('2029 - 2030', '2029 - 2030'),
    ]

    etudiant = models.OneToOneField(Etudiant, on_delete=models.CASCADE)
    date_nais = models.DateField(max_length=50)  # Ajoutez le champ date_nais
    genre = models.CharField(max_length=50)  # Ajoutez le champ genre
    telephone = models.CharField(max_length=20)  # Ajoutez le champ telephone
    objet_demande = models.CharField(max_length=50, choices=OBJET_CHOICES)
    session_dut = models.CharField(max_length=2, choices=SESSION_CHOICES_DUT, blank=True, null=True)
    session_lic = models.CharField(max_length=2, choices=SESSION_CHOICES_LICENCE, blank=True, null=True)
    annee_academique = models.CharField(max_length=50, choices=ANNEE_ACADEMIQUE_CHOICES)
    filiere = models.CharField(max_length=10)
    cycle = models.CharField(max_length=10)
    niveau = models.CharField(max_length=10)
    identite_receptioniste = models.ForeignKey(CSS, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        current_year = timezone.now().year

        # Récupérer l'étudiant associé à la demande
        etudiant = self.etudiant

        if not etudiant:
            raise ValidationError("Impossible de récupérer l'étudiant associé à la demande.")

        # Récupérer l'utilisateur connecté
        user = etudiant.user if etudiant else None

        if not user:
            raise ValidationError("Impossible de récupérer l'utilisateur connecté.")
        
        # Assigner les informations de l'utilisateur connecté
        self.identite_receptioniste = user.CSS  # Assurez-vous d'ajuster cela en fonction de votre modèle d'utilisateur

        # Assigner les informations de l'étudiant
        if int(self.annee_academique.split(' - ')[0]) > current_year:
            raise ValidationError("L'année académique ne peut pas être supérieure à l'année en cours.")
        
        if etudiant.cycle == 'DUT':
            self.session_lic = None
        elif etudiant.cycle == 'LICENCE':
            self.session_dut = None
        
        # Assigner les champs date_nais, genre et telephone
        self.date_nais = etudiant.date_nais
        self.genre = etudiant.genre
        self.telephone = etudiant.telephone
        self.filiere = etudiant.filiere
        self.cycle = etudiant.cycle
        self.niveau = etudiant.niveaux

        super(Demande, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.get_objet_demande_display()} - {self.session_dut or self.session_lic} - {self.filiere} - {self.cycle} - {self.annee_academique}'
