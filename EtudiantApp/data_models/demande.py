from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from EtudiantApp.data_models.etudiant import Etudiant
from CSSAPP.data_models.css import CSS
from EtudiantApp.data_models.notifications import Notification

from datetime import date


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

    MOIS_CHOICES = [
    ('janvier', 'Janvier'),
    ('février', 'Février'),
    ('mars', 'Mars'),
    ('avril', 'Avril'),
    ('mai', 'Mai'),
    ('juin', 'Juin'),
    ('juillet', 'Juillet'),
    ('août', 'Août'),
    ('septembre', 'Septembre'),
    ('octobre', 'Octobre'),
    ('novembre', 'Novembre'),
    ('décembre', 'Décembre'),
]
    

    ETATS_CHOICES = [
    ('En attente', 'En attente'),
    ('Acceptée', 'Acceptée'),
    ('En cours de traitement', 'En cours de traitement'),
    ('Terminée', 'Terminée'),
  
]


    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    date_nais = models.DateField(max_length=50)  # Ajoutez le champ date_nais
    genre = models.CharField(max_length=50)  # Ajoutez le champ genre
    telephone = models.CharField(max_length=20)  # Ajoutez le champ telephone
    objet_demande = models.CharField(max_length=50, choices=OBJET_CHOICES)
    session_dut = models.CharField(max_length=2, choices=SESSION_CHOICES_DUT, blank=True, null=True)
    session_lic = models.CharField(max_length=2, choices=SESSION_CHOICES_LICENCE, blank=True, null=True)
    annee_academique = models.CharField(max_length=50, choices=ANNEE_ACADEMIQUE_CHOICES)
    mois = models.CharField(max_length=50, choices=MOIS_CHOICES)
    filiere = models.CharField(max_length=12)
    cycle = models.CharField(max_length=12)
    niveau = models.CharField(max_length=12)
    date_poste_demande = models.DateField(default=date.today)
    date_de_mise_en_traitement = models.DateField(default=date.today)
    date_de_fin_treatment = models.DateField(default=date.today)
    date_refus = models.DateField(default=date.today)
    date_termine = models.DateField(default=date.today)
    etat = models.CharField(max_length=30, choices=ETATS_CHOICES, default='En attente')
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

        expediteur = self.etudiant
        destinataire = self.identite_receptioniste

        titre_poste = self.objet_demande  # Utilisez le champ approprié pour le titre du poste
        contenu_notification = f"L\'Etudiant  {expediteur.user.last_name} {expediteur.user.first_name} a fait une demande : {titre_poste}."
        date_creation = date.today()
        print(date_creation)
        print("Avant la création de la notification")
        notification = Notification(destinataire_css=destinataire, expediteur=expediteur ,  contenu=contenu_notification, date_creation=date_creation)
        notification.save()
        print("Après la création de la notification")


    def __str__(self):
        return f'{self.get_objet_demande_display()} - {self.session_dut or self.session_lic} - {self.filiere} - {self.cycle} - {self.annee_academique}'
