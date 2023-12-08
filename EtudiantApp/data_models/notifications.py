from django.db import models
from EtudiantApp.data_models.etudiant import Etudiant


class Notification(models.Model):
    destinataire = models.ForeignKey(Etudiant, on_delete=models.DO_NOTHING)
    contenu = models.TextField()
    est_lue = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']

    def marquer_comme_lue(self):
        self.est_lue = True
        self.save()