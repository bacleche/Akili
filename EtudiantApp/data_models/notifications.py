from django.db import models
from EtudiantApp.data_models.etudiant import Etudiant


class Notification(models.Model):
    destinataire = models.ForeignKey(Etudiant, on_delete=models.DO_NOTHING , related_name='notifications_destinataire')
    expediteur = models.ForeignKey(Etudiant, on_delete=models.DO_NOTHING, related_name='notifications_expediteur')
    contenu = models.TextField()
    est_lue = models.BooleanField(default=False)
    is_accept = models.BooleanField(default=False)
    is_refused = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']

    def marquer_comme_lue(self):
        self.est_lue = True
        self.save()

    def accepter_notification(self):
        self.is_accept = True
        self.marquer_comme_lue()
        self.save()

    def refuser_notification(self):
        self.is_refused = True
        self.marquer_comme_lue()
        self.save()