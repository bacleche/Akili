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
    identite = models.ForeignKey(Etudiant, on_delete=models.DO_NOTHING,  related_name='auteur_principal')
    co_auteur = models.ForeignKey(Etudiant, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='co_auteur')
    document = models.FileField(upload_to='memoires', max_length=500, validators=[validate_pdf_extension])

    def clean(self):
        # Assurez-vous que le co-auteur (s'il existe) est du même niveau, de la même filière et du même cycle
        if self.co_auteur:
            if (
                self.co_auteur.niveaux != self.identite.niveaux
                or self.co_auteur.cycle != self.identite.cycle
                or self.co_auteur.filiere != self.identite.filiere
            ):
                raise ValidationError("Le co-auteur doit être du même niveau, de la même filière et du même cycle.")

        existing_memoires = Memoire.objects.filter(
            models.Q(identite=self.identite) | models.Q(co_auteur=self.identite) |
            models.Q(identite=self.co_auteur) | models.Q(co_auteur=self.co_auteur)
        )
        
        # Vérifiez si un mémoire avec les mêmes identités existe déjà
        existing_memoires = Memoire.objects.filter(identite=self.identite, co_auteur=self.co_auteur)
        if self.pk:
            existing_memoires = existing_memoires.exclude(pk=self.pk)  # Exclure le mémoire actuel lors de la mise à jour

        if existing_memoires.exists():
            raise ValidationError("Vous ne pouvez publier qu'un seul mémoire avec ces identités.")
