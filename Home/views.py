from django.shortcuts import render,redirect
from EtudiantApp.data_models.memoire import Memoire
from EtudiantApp.data_models.etudiant import Etudiant


# Create your views here.
# def home_index(request):
#     matricules_etudiants = Etudiant.objects.values_list('Identification', flat=True)
#     memoires = Memoire.objects.filter(is_pubied=True, matricule_identification_binome__in=matricules_etudiants)
#     print(memoires)
#     # Récupérer les étudiants correspondant aux matricules_identification_binome des mémoires
#     etudiants_binomes = Etudiant.objects.filter(Identification__in=[memoire.matricule_identification_binome for memoire in memoires])
#     print(etudiants_binomes)
#     return render(request, 'index.html', context={'memoires': memoires, 'etudiants_binomes': etudiants_binomes})


def home_index(request):
    # Récupérer tous les mémoires publiés
    memoires_publies = Memoire.objects.filter(is_pubied=True)

    # Créer un dictionnaire pour stocker les mémoires avec leurs étudiants binômes
    memoires_etudiants = {}
    memoires_sans_binome = []

    # Récupérer les étudiants correspondant aux matricules_identification_binome des mémoires
    for memoire in memoires_publies:
        etudiant_binome = Etudiant.objects.filter(Identification=memoire.matricule_identification_binome).first()
        if etudiant_binome:
            memoires_etudiants[memoire] = etudiant_binome
        else:
            memoires_sans_binome.append(memoire)

    return render(request, 'index.html', context={'memoires_etudiants': memoires_etudiants, 'memoires_sans_binome': memoires_sans_binome})
