from django.shortcuts import render , redirect
from EtudiantApp.data_models.etudiant import Etudiant
from DCFISPACE.data_models.directeur import Directeur
from CSSAPP.data_models.documents import *
from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter
from django.conf import settings
import os
from django.db.models import Q
import shutil
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.pagesizes import letter
import PyPDF2
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from django.http import FileResponse
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
from django.urls import reverse
from django.views.decorators.http import require_http_methods


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('SignInView'))  # Redirige vers la page de connexion si l'utilisateur n'est pas connecté
        return view_func(request, *args, **kwargs)
    return wrapper




@login_required
@require_http_methods(["GET"])
def Home_Directeur(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification' , 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}
    print(user_data)
    return render(request, 'pages-dir/index-dcfi.html', user_data)


def Profiles_directeur(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}
    return render(request, 'pages-dir/profile-dcfi.html', user_data)



def profile_details_directeur(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}
    user_data['civilite_choices'] = Directeur._meta.get_field('civilite').choices
    return render(request, 'pages-dir/update-profiles-directeur.html', user_data)




def mis_a_jour_directeur(request):
    # Récupérez l'utilisateur actuel (CSS dans ce cas)
    user = Directeur.objects.get(matricule=request.session.get('matricule'))
    
    if request.method == 'POST':
        # Si la requête est de type POST, récupérez les données du formulaire
        user.user.last_name = request.POST.get('nom')
        user.user.first_name = request.POST.get('prenom')
        user.telephone = request.POST.get('phone')
        user.date_nais = request.POST.get('date')
        user.civilite = request.POST.get('civilite')
        user.role = request.POST.get('surname')  # Assurez-vous que le nom du champ correspond
        user.user.email = request.POST.get('email')
        user.role = request.POST.get('role')
        user.date_nais = request.POST.get('date_nais')
        pas1 = request.POST.get('password')
        pas2 = request.POST.get('password_conf')  # Utilisez set_password pour définir le mot de passe
          # Utilisez set_password pour définir le mot de passe
        if pas1 == pas2:
            if len(pas1) < 8 or len(pas2) < 8 : 
                print('ddddddeuueueueue')
                # return render(request, 'pages/profile-modify.html', {'user': user , 'error':'Aumoins 8 caractères'})
                messages.error(request, 'Au moins 8 caractères')
                return redirect('profile_details_directeur')
            user.user.set_password(request.POST.get('password'))
         
            # Gérez l'image de profil
            if 'new_profile_image' in request.FILES:
                image = request.FILES['new_profile_image']
                # Enregistrez l'image avec un nouveau nom pour éviter les collisions
                image_name = f"profile_image_{user.matricule}.{image.name.split('.')[-1]}"
                user.imagesprofiles.save(image_name, image)

            # Sauvegardez les modifications
            user.user.save()

            # Mettez à jour les données de la session avec les nouvelles valeurs
            request.session['nom'] = user.user.last_name
            request.session['prenom'] = user.user.first_name
            request.session['telephone'] = user.telephone
            request.session['date_nais'] = user.date_nais
            request.session['civilite'] = user.civilite
            request.session['role'] = user.role
            request.session['email'] = user.user.email
            request.session['genre'] = user.genre
            # request.session['mot_de_passe'] = user.mot_de_passe
            # request.session['confirmer_de_passe'] = user.confirmer_mot_de_passe
            request.session['imagesprofiles'] = user.imagesprofiles.url

            return redirect('Profiles_directeur')  # Redirigez vers la page de détails après la modification

        else:
            print('ddddddeuueueueue')
            messages.error(request, 'Les mots de passe doivent etre identiques')
            return redirect('profile_details_directeur')

    return render(request, 'pages-dir/update-profiles-directeur.html', {'user': user})

from django.core.paginator import Paginator

def liste_Attestations_directeur(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}
    

    # Filtrer les attestations avec is_transfer_directeur à True
    attestations = Attestation.objects.filter(is_transfer_directeur=True).order_by('-date_register')
    paginator = Paginator(attestations, 10)

    # Récupérer le numéro de la page à afficher, par défaut 1
    page_number = request.GET.get('page')
    
    # Récupérer les objets attestations pour la page donnée
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages-dir/liste_attestation_sign.html', {'attestations': attestations, 'user_data': user_data, 'page_obj':page_obj})




def liste_Bulletins_directeur(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    # Filtrer les attestations avec is_transfer_directeur à True
    bulletins = Bulletin.objects.filter(is_transfer_directeur=True).order_by('date_register')

    paginator = Paginator(bulletins, 10)

    # Récupérer le numéro de la page à afficher, par défaut 1
    page_number = request.GET.get('page')
    
    # Récupérer les objets attestations pour la page donnée
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages-dir/list_bulletins_sign.html', {'bulletins': bulletins, 'user_data': user_data, 'page_obj':page_obj})

# def signer_attestation(request, attestation_id):
#     # Récupérer l'objet Attestation
#     attestation = Attestation.objects.get(id=attestation_id)

#     # Ouvrir le PDF existant
#     existing_pdf = PdfReader(attestation.file)

#     # Créer un buffer pour stocker le PDF modifié
#     output_buffer = BytesIO()
#     pdf_writer = PdfWriter(output_buffer)

#     # Ajouter le texte à la première page du PDF existant
#     existing_page = existing_pdf.pages[0]
#     buffer = BytesIO()
#     c = canvas.Canvas(buffer, pagesize=letter)
#     c.drawString(100, 200, "Texte ajouté à l'attestation")  # Ajouter le texte à une position spécifique
#     c.save()
#     buffer.seek(0)
#     overlay_pdf = PdfReader(buffer)
#     existing_page.merge_page(overlay_pdf.pages[0])
#     pdf_writer.add_page(existing_page)

#     # Ajouter les autres pages du PDF existant sans modification
#     for page in existing_pdf.pages[1:]:
#         pdf_writer.add_page(page)

#     pdf_writer.write(output_buffer)
#     output_buffer.seek(0)

#     # Renvoyer le fichier PDF avec le texte ajouté
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(attestation.file.path)
#     response.write(output_buffer.getvalue())
#     return response


def signaler_css_attestation_directeur(request, attestation_id):
    attestation = Attestation.objects.get(id=attestation_id)
    attestation.is_transfer_css = True
    # attestation.save()
    date_poste = date.today()

    titre_poste = "Attestation Signé"  
    contenu_notification = f"{attestation.profile_directeur.user.last_name} {attestation.profile_directeur.user.first_name} vient d'appliquer une action  : {titre_poste}."
    date_creation = date_poste
    notification = Notification(destinataire_css=attestation.profiles_css, expediteur_dir=attestation.profile_directeur ,  contenu=contenu_notification, date_creation=date_creation )
    print('est arrivé')
    notification.save()
    print(notification)
    attestation.save()
    print('fifi')

    return redirect('liste_Attestations_directeur')

def signaler_css_bulletin_directeur(request, bulletin_id):
    bulletin = Bulletin.objects.get(id=bulletin_id)
    bulletin.is_transfer_css = True
    date_poste = date.today()

    titre_poste = "Bulletin Signé"  
    contenu_notification = f"{bulletin.profile_directeur.user.last_name} {bulletin.profile_directeur.user.first_name} vient d'appliquer une action  : {titre_poste}."
    date_creation = date_poste
    notification = Notification(destinataire_css=bulletin.profiles_css, expediteur_dir=bulletin.profile_directeur ,  contenu=contenu_notification, date_creation=date_creation )
    print('est arrivé')
    notification.save()
    print(notification)
    bulletin.save()
    print('fifi')
    return redirect('liste_Bulletins_directeur')


def signer_attestation(request, attestation_id):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    # Récupérer l'objet Attestation
    attestation = Attestation.objects.get(id=attestation_id)

    # Ouvrir le PDF existant
    existing_pdf = PdfReader(attestation.file.path)

    # Créer un buffer pour stocker le PDF modifié
    output_buffer = BytesIO()
    pdf_writer = PdfWriter(output_buffer)

    # Ajouter le texte à chaque page du PDF existant
    for page_number in range(len(existing_pdf.pages)):
        page = existing_pdf.pages[page_number]
        page_text = user_data['nom']+" "+user_data['prenom']+" Texte ajouté à l'attestation ✔️"
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 200, page_text)  # Ajouter le texte à une position spécifique sur chaque page
        c.save()
        buffer.seek(0)
        overlay_pdf = PdfReader(buffer)
        page.merge_page(overlay_pdf.pages[0])
        pdf_writer.add_page(page)

    # Écrire le PDF modifié dans le buffer
    pdf_writer.write(output_buffer)
    output_buffer.seek(0)

    # Écrire le contenu du buffer dans le fichier existant
    with open(attestation.file.path, 'wb') as file:
        file.write(output_buffer.getvalue())

    attestation.is_signed = True
    attestation.save()
    messages.success(request, "L'attestation a été signée avec succès.")
    # Rediriger vers une vue spécifique
    return redirect('liste_Attestations_directeur')


def attestation_text(text):
    # Créer un fichier PDF avec le texte spécifié
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    c.drawString(100, 750, text)  # Dessiner le texte sur le PDF
    c.save()
    
    # Retourner le contenu du PDF
    return  PdfReader(pdf_buffer)


def recherche_Attestations_directeur(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}
    q = request.GET.get('q')
    date = request.GET.get('date')

    # Filtrer les attestations en fonction de la recherche
    if q:
        attestations = Attestation.objects.filter(
            Q(etudiant__user__first_name__icontains=q) | Q(etudiant__user__last_name__icontains=q)
        )
    elif date:
        attestations = Attestation.objects.filter(date_register=date)
    else:
        attestations = Attestation.objects.all()

    return render(request, 'pages-dir/liste_attestation_sign.html', {'attestations': attestations, 'user_data': user_data})




def signer_buletins(request, bulletin_id):
    # Récupérer l'objet Attestation
    bulletin = Bulletin.objects.get(id=bulletin_id)

    # Ouvrir le PDF existant
    existing_pdf = PdfReader(bulletin.file.path)

    # Créer un buffer pour stocker le PDF modifié
    output_buffer = BytesIO()
    pdf_writer = PdfWriter(output_buffer)

    # Ajouter le texte à chaque page du PDF existant
    for page_number in range(len(existing_pdf.pages)):
        page = existing_pdf.pages[page_number]
        page_text = "Texte ajouté au bulletin  ✔️"
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 200, page_text)  # Ajouter le texte à une position spécifique sur chaque page
        c.save()
        buffer.seek(0)
        overlay_pdf = PdfReader(buffer)
        page.merge_page(overlay_pdf.pages[0])
        pdf_writer.add_page(page)

    # Écrire le PDF modifié dans le buffer
    pdf_writer.write(output_buffer)
    output_buffer.seek(0)

    # Écrire le contenu du buffer dans le fichier existant
    with open(bulletin.file.path, 'wb') as file:
        file.write(output_buffer.getvalue())

    bulletin.is_signed = True
    bulletin.save()
    messages.success(request, "Le Bulletin  a été signée avec succès.")
    # Rediriger vers une vue spécifique
    return redirect('liste_Bulletins_directeur')



def recherche_Bulletins_directeur(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}
    q = request.GET.get('q')
    date = request.GET.get('date')

    # Filtrer les attestations en fonction de la recherche
    if q:
        bulletins = Bulletin.objects.filter(
            Q(etudiant__user__first_name__icontains=q) | Q(etudiant__user__last_name__icontains=q)
        )
    elif date:
        bulletins = Bulletin.objects.filter(date_register=date)
    else:
        bulletins = Bulletin.objects.all()

    return render(request, 'pages-dir/list_bulletins_sign.html', {'bulletins': bulletins, 'user_data': user_data})







def imprimer_attestations_directeur(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    # Récupérer toutes les attestations à imprimer
    attestations = Attestation.objects.all()  # Assurez-vous de remplacer VotreModele par votre propre modèle
    datey = date.today()
    # Charger le template HTML
    template_path = 'pages-dir/imprimer_attestation_directeur.html'
    template = get_template(template_path)
    
    # Remplir le template avec les données des attestations
    context = {'attestations': attestations, 'user_data': user_data , 'datey':datey}
    html = template.render(context)

    # Générer le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="liste_attestations.pdf"'
    
    # Convertir le HTML en PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Vérifier si la conversion s'est bien déroulée
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    
    return response



def imprimer_bulletins_directeur(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    # Récupérer toutes les attestations à imprimer
    bulletins = Bulletin.objects.all()  # Assurez-vous de remplacer VotreModele par votre propre modèle
    datey = date.today()
    # Charger le template HTML
    template_path = 'pages-dir/imprimer_bulletins_directeur.html'
    template = get_template(template_path)
    
    # Remplir le template avec les données des attestations
    context = {'bulletins': bulletins, 'user_data': user_data , 'datey':datey}
    html = template.render(context)

    # Générer le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="liste_bulletins.pdf"'
    
    # Convertir le HTML en PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Vérifier si la conversion s'est bien déroulée
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    
    return response







# def supprimer_bulletin_directeur(request):

#     user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}

#     bulletin = Bulletin.objects.all().delete()
#     context = {'user_data':user_data}
#     return redirect('liste_Bulletins_directeur')