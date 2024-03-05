from django.shortcuts import render,redirect
from EtudiantApp.data_models.memoire import Memoire

# Create your views here.


def home_index(request):
    memoires = Memoire.objects.filter(is_pubied=True)  # Assurez-vous d'utiliser "objects" au lieu de "Object"
    return render(request, 'index.html', context={'memoires': memoires})