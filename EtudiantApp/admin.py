from django.contrib import admin

from EtudiantApp.data_models.etudiant import Etudiant
from EtudiantApp.data_models.demande import Demande
from EtudiantApp.data_models.memoire import Memoire


admin.site.register(Etudiant)
admin.site.register(Demande)
admin.site.register(Memoire)


# Register your models here.
