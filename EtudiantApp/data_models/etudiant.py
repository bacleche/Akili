from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError




CIVILITE_CHOICES = [
    ('marié', 'MARIE'),
    ('veuf(ve)', 'VEUF(VE)'),
    ('célibataire', 'CELIBATAIRE'),
]

NIVEAUX_CHOICES = [
    ('licence1', 'LICENCE1'),
    ('licence2', 'LICENCE2'),
    ('licence3', 'LICENCE3'),
    ('dut1', 'DUT1'),
    ('dut2', 'DUT2')
]

CYCLE_CHOICES = [ 
    ('licence', 'LICENCE'),
    ('dut', 'DUT'),
]

FILIERE_CHOICES = [ 
    ('informatique', 'INFORMATIQUE'),
    ('administration', 'ADMINISTRATION'),
]

STATUT_CHOICES = [
    ('En Frequentation', 'En Fréquentation'),
    ('Ancien etudiant', 'Ancien étudiant'),
]

MOIS_CHOICES = [
    (1, 'Janvier'),
    (2, 'Février'),
    (3, 'Mars'),
    (4, 'Avril'),
    (5, 'Mai'),
    (6, 'Juin'),
    (7, 'Juillet'),
    (8, 'Août'),
    (9, 'Septembre'),
    (10, 'Octobre'),
    (11, 'Novembre'),
    (12, 'Décembre'),
]

class Etudiant(models.Model):
    # Vos autres champs

    matricule = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
    date_nais = models.DateField()
    civilite = models.CharField(max_length=20, choices=CIVILITE_CHOICES , default='Célibataire')
    cycle = models.CharField(max_length=20, choices=CYCLE_CHOICES , default='licence')
    filiere = models.CharField(max_length=20, choices=FILIERE_CHOICES , default='informatique')
    niveaux = models.CharField(max_length=20, choices=NIVEAUX_CHOICES , default='licence1')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES , default='En Frequentation')
    mois_debut_annee_academique = models.IntegerField(choices=MOIS_CHOICES, default=9)  # Choisissez le mois de début de l'année académique
    annee_academique = models.CharField(max_length=9, default=None)  # Champ pour l'année académique au format "AAAA - AAAA"
    annee_frequentation_fin = models.DateField(default=None)
    email = models.EmailField(unique=True , default=None)
    genre = models.CharField(max_length=10, choices=[('Homme', 'Homme'), ('Femme', 'Femme')] , default='Homme')
    mot_de_passe = models.CharField(max_length=255 , default=None)
    confirmer_mot_de_passe = models.CharField(max_length=255 , default=None)
    imagesprofiles = models.ImageField(upload_to='images/',max_length=500,default='../static/assets_dash/r.jpg') 
    


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
        

        self.update_annee_academique()
        super(Etudiant, self).save(*args, **kwargs)

    def generate_matricule(self):
        last_etudiant = Etudiant.objects.order_by('-matricule').first()
        if last_etudiant:
            last_matricule = last_etudiant.matricule
            matricule_number = int(last_matricule[1:]) + 1
        else:
            matricule_number = 1
        return f'M{matricule_number:06d}'
    
    def update_annee_academique(self):
        current_year = timezone.now().year
        current_month = timezone.now().month

        # Utilisez le mois de début de l'année académique spécifié
        start_month = self.mois_debut_annee_academique

        # Calculez l'année académique en fonction de la durée de 10 mois
        if current_month >= start_month:
            start_year = current_year
            end_year = current_year + 1
        else:
            start_year = current_year - 1
            end_year = current_year

@receiver(pre_save, sender=Etudiant)
def etudiant_pre_save(sender, instance, **kwargs):
    if not instance.matricule:
        instance.matricule = instance.generate_matricule()


    if instance.annee_frequentation_fin is not None:
        current_year = timezone.now().year
        if instance.annee_frequentation_fin == current_year:
            instance.statut = 'Ancien etudiant'