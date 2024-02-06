from django.shortcuts import render , redirect
from EtudiantApp.data_models.etudiant import Etudiant
# from .forms import *
from django.contrib import messages
from Utilisateur.data_models.utilisateur import Utilisateur
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from EtudiantApp.data_models.notifications import Notification
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from datetime import date
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def Home_Directeur(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification' , 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}
    print(user_data)
    return render(request, 'pages-dir/index-dcfi.html', user_data)
