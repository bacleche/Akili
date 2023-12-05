from django.db import models
from datetime import date
from EtudiantApp.data_models.etudiant import Etudiant
from django.core.exceptions import ValidationError

def validate_pdf_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Le document doit être au format PDF.')

class Memoire(models.Model):
    # Vos autres champs
    Id_mem = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=255)
    date_poste = models.DateField(default=date.today)
    identite = models.ForeignKey(Etudiant, on_delete=models.DO_NOTHING, related_name='auteur_principal')
    matricule_identification_binome = models.CharField(max_length=20, blank=True, null=True)
    document = models.FileField(upload_to='memoires', max_length=500, validators=[validate_pdf_extension])

    def clean(self):
        # Assurez-vous que le matricule_identification_binome existe et est correct
        if self.matricule_identification_binome:
            try:
                binome = Etudiant.objects.get(Identification=self.matricule_identification_binome)
                # Ajoutez d'autres vérifications si nécessaire
            except Etudiant.DoesNotExist:
                raise ValidationError("Le matricule d'identification du binôme est incorrect.")
        else:
            binome = None

        existing_memoires = Memoire.objects.filter(
            models.Q(identite=self.identite) |
            models.Q(matricule_identification_binome=self.matricule_identification_binome) |
            (models.Q(identite=binome) if binome else models.Q()) |
            (models.Q(matricule_identification_binome=binome.Identification) if binome and binome.Identification else models.Q())
        )
        
        # Vérifiez si un mémoire avec les mêmes identités existe déjà
        existing_memoires = existing_memoires.exclude(pk=self.pk) if self.pk else existing_memoires
        if existing_memoires.exists():
            raise ValidationError("Vous ne pouvez publier qu'un seul mémoire avec ces identités.")
