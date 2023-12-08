from django.contrib import admin

from EtudiantApp.data_models.etudiant import Etudiant
from EtudiantApp.data_models.demande import Demande
from EtudiantApp.data_models.memoire import Memoire
from EtudiantApp.data_models.notifications import Notification



admin.site.register(Etudiant)
admin.site.register(Demande)
admin.site.register(Memoire)
admin.site.register(Notification)



# Register your models here.
