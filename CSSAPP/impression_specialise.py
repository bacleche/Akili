from django.shortcuts import render , redirect
from CSSAPP.data_models.css import CSS
from CSSAPP.data_models.documents import Attestation , Bulletin
from EtudiantApp.data_models.demande import Demande
from EtudiantApp.data_models.etudiant import Etudiant
from django.db.models import Q
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import logout
import csv
from datetime import date
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
# Create your views here.

from django.shortcuts import redirect
from django.contrib import messages





def imprimer_etudiant_lic1(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    # Récupérer toutes les attestations à imprimer
    etudiants = Etudiant.objects.filter(cycle='licence', niveaux='licence1', filiere='informatique', statut='En Fréquentation')  # Assurez-vous de remplacer VotreModele par votre propre modèle
    datey = date.today()
    # Charger le template HTML
    template_path = 'pages/impression_etudiants_toute_categories.html'
    template = get_template(template_path)
    
    # Remplir le template avec les données des attestations
    context = {'etudiants': etudiants, 'user_data': user_data , 'datey':datey}
    html = template.render(context)

    # Générer le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="listes_des_etudiants_lic1.pdf"'
    
    # Convertir le HTML en PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Vérifier si la conversion s'est bien déroulée
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    
    return response






def imprimer_etudiant_lic2(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    # Récupérer toutes les attestations à imprimer
    etudiants = Etudiant.objects.filter(cycle='licence', niveaux='licence2', filiere='informatique', statut='En Fréquentation')  # Assurez-vous de remplacer VotreModele par votre propre modèle
    datey = date.today()
    # Charger le template HTML
    template_path = 'pages/impression_etudiants_toute_categories.html'
    template = get_template(template_path)
    
    # Remplir le template avec les données des attestations
    context = {'etudiants': etudiants, 'user_data': user_data , 'datey':datey}
    html = template.render(context)

    # Générer le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="listes_des_etudiants_lic2.pdf"'
    
    # Convertir le HTML en PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Vérifier si la conversion s'est bien déroulée
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    
    return response





def imprimer_etudiant_lic3(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    # Récupérer toutes les attestations à imprimer
    etudiants = Etudiant.objects.filter(cycle='licence', niveaux='licence3', filiere='informatique', statut='En Fréquentation')  # Assurez-vous de remplacer VotreModele par votre propre modèle
    datey = date.today()
    # Charger le template HTML
    template_path = 'pages/impression_etudiants_toute_categories.html'
    template = get_template(template_path)
    
    # Remplir le template avec les données des attestations
    context = {'etudiants': etudiants, 'user_data': user_data , 'datey':datey}
    html = template.render(context)

    # Générer le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="listes_des_etudiants_lic3.pdf"'
    
    # Convertir le HTML en PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Vérifier si la conversion s'est bien déroulée
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    
    return response











def imprimer_etudiant_admin1(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    # Récupérer toutes les attestations à imprimer
    etudiants = Etudiant.objects.filter(cycle='licence', niveaux='licence1', filiere='administration', statut='En Fréquentation')  # Assurez-vous de remplacer VotreModele par votre propre modèle
    datey = date.today()
    # Charger le template HTML
    template_path = 'pages/impression_etudiants_toute_categories.html'
    template = get_template(template_path)
    
    # Remplir le template avec les données des attestations
    context = {'etudiants': etudiants, 'user_data': user_data , 'datey':datey}
    html = template.render(context)

    # Générer le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="listes_des_etudiants_admin1.pdf"'
    
    # Convertir le HTML en PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Vérifier si la conversion s'est bien déroulée
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    
    return response



def imprimer_etudiant_admin2(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    # Récupérer toutes les attestations à imprimer
    etudiants = Etudiant.objects.filter(cycle='licence', niveaux='licence2', filiere='administration', statut='En Fréquentation')  # Assurez-vous de remplacer VotreModele par votre propre modèle
    datey = date.today()
    # Charger le template HTML
    template_path = 'pages/impression_etudiants_toute_categories.html'
    template = get_template(template_path)
    
    # Remplir le template avec les données des attestations
    context = {'etudiants': etudiants, 'user_data': user_data , 'datey':datey}
    html = template.render(context)

    # Générer le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="listes_des_etudiants_admin2.pdf"'
    
    # Convertir le HTML en PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Vérifier si la conversion s'est bien déroulée
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    
    return response




def imprimer_etudiant_admin3(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    # Récupérer toutes les attestations à imprimer
    etudiants = Etudiant.objects.filter(cycle='licence', niveaux='licence3', filiere='administration', statut='En Fréquentation')  # Assurez-vous de remplacer VotreModele par votre propre modèle
    datey = date.today()
    # Charger le template HTML
    template_path = 'pages/impression_etudiants_toute_categories.html'
    template = get_template(template_path)
    
    # Remplir le template avec les données des attestations
    context = {'etudiants': etudiants, 'user_data': user_data , 'datey':datey}
    html = template.render(context)

    # Générer le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="listes_des_etudiants_admin3.pdf"'
    
    # Convertir le HTML en PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Vérifier si la conversion s'est bien déroulée
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    
    return response




def imprimer_etudiant_dut_admin1(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    # Récupérer toutes les attestations à imprimer
    etudiants = Etudiant.objects.filter(cycle='dut', niveaux='dut1', filiere='administration', statut='En Fréquentation')  # Assurez-vous de remplacer VotreModele par votre propre modèle
    datey = date.today()
    # Charger le template HTML
    template_path = 'pages/impression_etudiants_toute_categories.html'
    template = get_template(template_path)
    
    # Remplir le template avec les données des attestations
    context = {'etudiants': etudiants, 'user_data': user_data , 'datey':datey}
    html = template.render(context)

    # Générer le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="listes_des_etudiants_dut_admin1.pdf"'
    
    # Convertir le HTML en PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Vérifier si la conversion s'est bien déroulée
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    
    return response





def imprimer_etudiant_dut_admin2(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    # Récupérer toutes les attestations à imprimer
    etudiants = Etudiant.objects.filter(cycle='dut', niveaux='dut2', filiere='administration', statut='En Fréquentation')  # Assurez-vous de remplacer VotreModele par votre propre modèle
    datey = date.today()
    # Charger le template HTML
    template_path = 'pages/impression_etudiants_toute_categories.html'
    template = get_template(template_path)
    
    # Remplir le template avec les données des attestations
    context = {'etudiants': etudiants, 'user_data': user_data , 'datey':datey}
    html = template.render(context)

    # Générer le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="listes_des_etudiants_dut_admin2.pdf"'
    
    # Convertir le HTML en PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Vérifier si la conversion s'est bien déroulée
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    
    return response




def imprimer_etudiant_dut_informatique1(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    # Récupérer toutes les attestations à imprimer
    etudiants = Etudiant.objects.filter(cycle='dut', niveaux='dut1', filiere='informatique', statut='En Fréquentation')  # Assurez-vous de remplacer VotreModele par votre propre modèle
    datey = date.today()
    # Charger le template HTML
    template_path = 'pages/impression_etudiants_toute_categories.html'
    template = get_template(template_path)
    
    # Remplir le template avec les données des attestations
    context = {'etudiants': etudiants, 'user_data': user_data , 'datey':datey}
    html = template.render(context)

    # Générer le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="listes_des_etudiants_dut_info1.pdf"'
    
    # Convertir le HTML en PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Vérifier si la conversion s'est bien déroulée
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    
    return response




def imprimer_etudiant_dut_informatique2(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    # Récupérer toutes les attestations à imprimer
    etudiants = Etudiant.objects.filter(cycle='dut', niveaux='dut2', filiere='informatique', statut='En Fréquentation')  # Assurez-vous de remplacer VotreModele par votre propre modèle
    datey = date.today()
    # Charger le template HTML
    template_path = 'pages/impression_etudiants_toute_categories.html'
    template = get_template(template_path)
    
    # Remplir le template avec les données des attestations
    context = {'etudiants': etudiants, 'user_data': user_data , 'datey':datey}
    html = template.render(context)

    # Générer le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="listes_des_etudiants_dut_info2.pdf"'
    
    # Convertir le HTML en PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Vérifier si la conversion s'est bien déroulée
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    
    return response