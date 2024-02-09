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

def create_document_lic1_info(request, etudiant_id):
    etudiant = Etudiant.objects.get(id=etudiant_id)

    if request.method == 'POST':
        type_attestation = request.POST.get('type_attestation')
        document = request.POST.get('document')
        date_regis = date.today()
        docs = request.FILES.get('docs')
        
        if document == 'attestation':
            # Créer une nouvelle attestation pour l'étudiant
            Attestation.objects.create(
                etudiant=etudiant,
                types_attestation=type_attestation,
                date_register=date_regis,
                file=docs,
                is_transfer_directeur = True,
                # Ajoutez d'autres champs spécifiques à l'attestation ici...
            )
            messages.success(request, 'Attestation créée avec succès.')
        elif document == 'bulletin':
            # Créer un nouveau bulletin pour l'étudiant
            Bulletin.objects.create(
                etudiant=etudiant,
                date_register=date_regis,
                file=docs,
                # Ajoutez d'autres champs spécifiques au bulletin ici...
            )
            messages.success(request, 'Bulletin créé avec succès.')

        return redirect('liste_etudiants_licence')

    messages.error(request, 'JAMAIS')
    return redirect('liste_etudiants_licence')
    




def create_document_lic2_info(request, etudiant_id):
    etudiant = Etudiant.objects.get(id=etudiant_id)

    if request.method == 'POST':
        type_attestation = request.POST.get('type_attestation')
        document = request.POST.get('document')
        date_regis = date.today()
        docs = request.FILES.get('docs')
        
        if document == 'attestation':
            # Créer une nouvelle attestation pour l'étudiant
            Attestation.objects.create(
                etudiant=etudiant,
                types_attestation=type_attestation,
                date_register=date_regis,
                file=docs,
                # Ajoutez d'autres champs spécifiques à l'attestation ici...
            )
            messages.success(request, 'Attestation créée avec succès.')
        elif document == 'bulletin':
            # Créer un nouveau bulletin pour l'étudiant
            Bulletin.objects.create(
                etudiant=etudiant,
                date_register=date_regis,
                file=docs,
                # Ajoutez d'autres champs spécifiques au bulletin ici...
            )
            messages.success(request, 'Bulletin créé avec succès.')

        return redirect('liste_etudiants_licence_info2')

    messages.error(request, 'JAMAIS')
    return redirect('liste_etudiants_licence_info2')
    




def create_document_lic3_info(request, etudiant_id):
    etudiant = Etudiant.objects.get(id=etudiant_id)

    if request.method == 'POST':
        type_attestation = request.POST.get('type_attestation')
        document = request.POST.get('document')
        date_regis = date.today()
        docs = request.FILES.get('docs')
        
        if document == 'attestation':
            # Créer une nouvelle attestation pour l'étudiant
            Attestation.objects.create(
                etudiant=etudiant,
                types_attestation=type_attestation,
                date_register=date_regis,
                file=docs,
                # Ajoutez d'autres champs spécifiques à l'attestation ici...
            )
            messages.success(request, 'Attestation créée avec succès.')
        elif document == 'bulletin':
            # Créer un nouveau bulletin pour l'étudiant
            Bulletin.objects.create(
                etudiant=etudiant,
                date_register=date_regis,
                file=docs,
                # Ajoutez d'autres champs spécifiques au bulletin ici...
            )
            messages.success(request, 'Bulletin créé avec succès.')

        return redirect('liste_etudiants_licence_info3')

    messages.error(request, 'JAMAIS')
    return redirect('liste_etudiants_licence_info3')
    





def create_document_lic1_admin(request, etudiant_id):
    etudiant = Etudiant.objects.get(id=etudiant_id)

    if request.method == 'POST':
        type_attestation = request.POST.get('type_attestation')
        document = request.POST.get('document')
        date_regis = date.today()
        docs = request.FILES.get('docs')
        
        if document == 'attestation':
            # Créer une nouvelle attestation pour l'étudiant
            Attestation.objects.create(
                etudiant=etudiant,
                types_attestation=type_attestation,
                date_register=date_regis,
                file=docs,
                # Ajoutez d'autres champs spécifiques à l'attestation ici...
            )
            messages.success(request, 'Attestation créée avec succès.')
        elif document == 'bulletin':
            # Créer un nouveau bulletin pour l'étudiant
            Bulletin.objects.create(
                etudiant=etudiant,
                date_register=date_regis,
                file=docs,
                # Ajoutez d'autres champs spécifiques au bulletin ici...
            )
            messages.success(request, 'Bulletin créé avec succès.')

        return redirect('liste_etudiants_licence_admin1')

    messages.error(request, 'JAMAIS')
    return redirect('liste_etudiants_licence_admin1')
    






def create_document_lic2_admin(request, etudiant_id):
    etudiant = Etudiant.objects.get(id=etudiant_id)

    if request.method == 'POST':
        type_attestation = request.POST.get('type_attestation')
        document = request.POST.get('document')
        date_regis = date.today()
        docs = request.FILES.get('docs')
        
        if document == 'attestation':
            # Créer une nouvelle attestation pour l'étudiant
            Attestation.objects.create(
                etudiant=etudiant,
                types_attestation=type_attestation,
                date_register=date_regis,
                file=docs,
                # Ajoutez d'autres champs spécifiques à l'attestation ici...
            )
            messages.success(request, 'Attestation créée avec succès.')
        elif document == 'bulletin':
            # Créer un nouveau bulletin pour l'étudiant
            Bulletin.objects.create(
                etudiant=etudiant,
                date_register=date_regis,
                file=docs,
                # Ajoutez d'autres champs spécifiques au bulletin ici...
            )
            messages.success(request, 'Bulletin créé avec succès.')

        return redirect('liste_etudiants_licence_admin2')

    messages.error(request, 'JAMAIS')
    return redirect('liste_etudiants_licence_admin2')
    




def create_document_lic3_admin(request, etudiant_id):
    etudiant = Etudiant.objects.get(id=etudiant_id)

    if request.method == 'POST':
        type_attestation = request.POST.get('type_attestation')
        document = request.POST.get('document')
        date_regis = date.today()
        docs = request.FILES.get('docs')
        
        if document == 'attestation':
            # Créer une nouvelle attestation pour l'étudiant
            Attestation.objects.create(
                etudiant=etudiant,
                types_attestation=type_attestation,
                date_register=date_regis,
                file=docs,
                # Ajoutez d'autres champs spécifiques à l'attestation ici...
            )
            messages.success(request, 'Attestation créée avec succès.')
        elif document == 'bulletin':
            # Créer un nouveau bulletin pour l'étudiant
            Bulletin.objects.create(
                etudiant=etudiant,
                date_register=date_regis,
                file=docs,
                # Ajoutez d'autres champs spécifiques au bulletin ici...
            )
            messages.success(request, 'Bulletin créé avec succès.')

        return redirect('liste_etudiants_licence_admin3')

    messages.error(request, 'JAMAIS')
    return redirect('liste_etudiants_licence_admin3')
    






def create_document_dut1_admin(request, etudiant_id):
    etudiant = Etudiant.objects.get(id=etudiant_id)

    if request.method == 'POST':
        type_attestation = request.POST.get('type_attestation')
        document = request.POST.get('document')
        date_regis = date.today()
        docs = request.FILES.get('docs')
        
        if document == 'attestation':
            # Créer une nouvelle attestation pour l'étudiant
            Attestation.objects.create(
                etudiant=etudiant,
                types_attestation=type_attestation,
                date_register=date_regis,
                file=docs,
                # Ajoutez d'autres champs spécifiques à l'attestation ici...
            )
            messages.success(request, 'Attestation créée avec succès.')
        elif document == 'bulletin':
            # Créer un nouveau bulletin pour l'étudiant
            Bulletin.objects.create(
                etudiant=etudiant,
                date_register=date_regis,
                file=docs,
                # Ajoutez d'autres champs spécifiques au bulletin ici...
            )
            messages.success(request, 'Bulletin créé avec succès.')

        return redirect('liste_etudiants_administration_dut1')

    messages.error(request, 'JAMAIS')
    return redirect('liste_etudiants_administration_dut1')
    





def create_document_dut2_admin(request, etudiant_id):
    etudiant = Etudiant.objects.get(id=etudiant_id)

    if request.method == 'POST':
        type_attestation = request.POST.get('type_attestation')
        document = request.POST.get('document')
        date_regis = date.today()
        docs = request.FILES.get('docs')
        
        if document == 'attestation':
            # Créer une nouvelle attestation pour l'étudiant
            Attestation.objects.create(
                etudiant=etudiant,
                types_attestation=type_attestation,
                date_register=date_regis,
                file=docs,
                # Ajoutez d'autres champs spécifiques à l'attestation ici...
            )
            messages.success(request, 'Attestation créée avec succès.')
        elif document == 'bulletin':
            # Créer un nouveau bulletin pour l'étudiant
            Bulletin.objects.create(
                etudiant=etudiant,
                date_register=date_regis,
                file=docs,
                # Ajoutez d'autres champs spécifiques au bulletin ici...
            )
            messages.success(request, 'Bulletin créé avec succès.')

        return redirect('liste_etudiants_administration_dut2')

    messages.error(request, 'JAMAIS')
    return redirect('liste_etudiants_administration_dut2')
    




def create_document_dut2_info(request, etudiant_id):
    etudiant = Etudiant.objects.get(id=etudiant_id)

    if request.method == 'POST':
        type_attestation = request.POST.get('type_attestation')
        document = request.POST.get('document')
        date_regis = date.today()
        docs = request.FILES.get('docs')
        
        if document == 'attestation':
            # Créer une nouvelle attestation pour l'étudiant
            Attestation.objects.create(
                etudiant=etudiant,
                types_attestation=type_attestation,
                date_register=date_regis,
                file=docs,
                # Ajoutez d'autres champs spécifiques à l'attestation ici...
            )
            messages.success(request, 'Attestation créée avec succès.')
        elif document == 'bulletin':
            # Créer un nouveau bulletin pour l'étudiant
            Bulletin.objects.create(
                etudiant=etudiant,
                date_register=date_regis,
                file=docs,
                # Ajoutez d'autres champs spécifiques au bulletin ici...
            )
            messages.success(request, 'Bulletin créé avec succès.')

        return redirect('liste_etudiants_dut_info2')

    messages.error(request, 'JAMAIS')
    return redirect('liste_etudiants_dut_info2')
    


def create_document_dut1_info(request, etudiant_id):
    etudiant = Etudiant.objects.get(id=etudiant_id)

    if request.method == 'POST':
        type_attestation = request.POST.get('type_attestation')
        document = request.POST.get('document')
        date_regis = date.today()
        docs = request.FILES.get('docs')
        
        if document == 'attestation':
            # Créer une nouvelle attestation pour l'étudiant
            Attestation.objects.create(
                etudiant=etudiant,
                types_attestation=type_attestation,
                date_register=date_regis,
                file=docs,
                # Ajoutez d'autres champs spécifiques à l'attestation ici...
            )
            messages.success(request, 'Attestation créée avec succès.')
        elif document == 'bulletin':
            # Créer un nouveau bulletin pour l'étudiant
            Bulletin.objects.create(
                etudiant=etudiant,
                date_register=date_regis,
                file=docs,
                # Ajoutez d'autres champs spécifiques au bulletin ici...
            )
            messages.success(request, 'Bulletin créé avec succès.')

        return redirect('liste_etudiants_dut_info1')

    messages.error(request, 'JAMAIS')
    return redirect('liste_etudiants_dut_info1')
    