from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError
from Utilisateur.data_models.utilisateur import Utilisateur, UtilisateurManager


class EtudiantManager(UtilisateurManager):
    pass


NIVEAUX_CHOICES = [
    ('licence1', 'LICENCE1'),
    ('licence2', 'LICENCE2'),
    ('licence3', 'LICENCE3'),
    ('dut1', 'DUT1'),
    ('dut2', 'DUT2'),
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
    ('En Fréquentation', 'En Fréquentation'),
    ('Ancien étudiant', 'Ancien étudiant'),
]

ANNEE_ACADEMIQUE_CHOICES = [
    ('2022 - 2023', '2022 - 2023'),
    ('2023 - 2024', '2023 - 2024'),
    ('2024 - 2025', '2024 - 2025'),
    ('2025 - 2026', '2025 - 2026'),
    ('2026 - 2027', '2026 - 2027'),
    ('2027 - 2028', '2027 - 2028'),
    ('2028 - 2029', '2028 - 2029'),
    ('2029 - 2030', '2029 - 2030'),
]

class Etudiant(Utilisateur):
    matricule = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    Identification = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    cycle = models.CharField(max_length=20, choices=CYCLE_CHOICES, default='licence')
    filiere = models.CharField(max_length=20, choices=FILIERE_CHOICES, default='informatique')
    niveaux = models.CharField(max_length=20, choices=NIVEAUX_CHOICES, default='licence1')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='En Fréquentation')
    a_soutenu = models.BooleanField(default=False)
    annee_academique = models.CharField(max_length=19, choices=ANNEE_ACADEMIQUE_CHOICES, default='2023 - 2024')
    annee_frequentation_fin = models.DateField(blank=True, null=True)

    objects = EtudiantManager()

    def save(self, *args, **kwargs):
        if not self.matricule:
            self.matricule = self.generate_matricule()
            self.Identification = self.generate_identification()

        self.clean()

        self.update_annee_academique()  # Appel de la méthode pour mettre à jour l'année académique
        super(Etudiant, self).save(*args, **kwargs)
    def generate_matricule(self):
        last_etudiant = Etudiant.objects.order_by('-matricule').first()

        if last_etudiant:
            last_matricule = last_etudiant.matricule
            matricule_number = int(last_matricule[1:]) + 1
        else:
            matricule_number = 1
        return f'M{matricule_number:06d}'

    def generate_identification(self):
        last_etudiant_identifie = Etudiant.objects.order_by('-Identification').first()

        if last_etudiant_identifie:
            last_identification = last_etudiant_identifie.Identification
            indent_number = int(last_identification[1:]) + 1
        else:
            indent_number = 1

        return f'I{indent_number:06d}'

    def update_annee_academique(self):
        if not self.annee_academique:  # N'actualise l'année académique que si elle est vide
                current_year = timezone.now().year
                start_year = current_year
                end_year = current_year + 1
                self.annee_academique = f'{start_year} - {end_year}'


    def clean(self):
        super().clean()
        if self.cycle == 'licence' and self.niveaux.startswith('dut'):
            raise ValidationError("A student in the 'licence' cycle cannot have a DUT level.")
        elif self.cycle == 'dut' and self.niveaux.startswith('licence'):
            raise ValidationError("A student in the 'DUT' cycle cannot have a 'licence' level.")

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"


@receiver(pre_save, sender=Etudiant)
def etudiant_pre_save(sender, instance, **kwargs):
    if not instance.matricule and not instance.Identification:
        instance.matricule = instance.generate_matricule()
        instance.Identification = instance.generate_identification()

    if instance.annee_frequentation_fin is not None:
        current_year = timezone.now().year
        if instance.annee_frequentation_fin == current_year:
            instance.statut = 'Ancien étudiant'
