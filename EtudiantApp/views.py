from django.shortcuts import render , redirect
from EtudiantApp.data_models.etudiant import Etudiant
from CSSAPP.data_models.documents import *
import os
import shutil
from django.conf import settings
from django.db.models import Q
from datetime import datetime

from .forms import *
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
def EtudiantSPACE(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification' , 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}
    print(user_data)
    return render(request, 'pages/index.html', user_data)

def Profiles_etudiant(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification' , 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}
    return render(request, 'pages/profile-etudiant.html', user_data)

def profile_details_etudiant(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification' , 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}
    user_data['civilite_choices'] = Etudiant._meta.get_field('civilite').choices
    return render(request, 'pages/profile-modify-etudiant.html', user_data)


def mis_a_jour_etudiant(request):
    # Récupérez l'utilisateur actuel (CSS dans ce cas)
    user = Etudiant.objects.get(matricule=request.session.get('matricule'))
    
    
    
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

            return redirect('Profiles_etudiant')  # Redirigez vers la page de détails après la modification
        else:
            print('ddddddeuueueueue')
            return render(request, 'pages/profile-modify-etudiant.html', {'user': user , 'error':'non'})

    return render(request, 'pages/profile-modify-etudiant.html', {'user': user})



# def poster_memoire(request):
#     user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles' , 'cycle', 'filiere' , 'niveaux']}
    
#     if request.method == 'POST':
#         form = MemoireForm(request.POST, request.FILES, user_data=user_data)
#         if form.is_valid():
#             form.save()
#             return redirect('poster_memoire')
#     else:
#         form = MemoireForm(user_data=user_data)
        

#     return render(request, 'pages/memoire-posts.html', {'form': form, 'user_data': user_data})

def poster_memoire(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles' , 'cycle', 'filiere' , 'niveaux']}
    
    if request.method == 'POST':
        form = MemoireForm(request.POST, request.FILES, user_data=user_data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le mémoire a été posté avec succès!')
            return redirect('poster_memoire')           
    else:
        form = MemoireForm(user_data=user_data)

    return render(request, 'pages/memoire-posts.html', {'form': form, 'user_data': user_data})

def creer_demande(request):
    user_data = {
        'matricule': request.session.get('matricule'),
        'Identification': request.session.get('Identification'),
        'nom': request.session.get('nom'),
        'prenom': request.session.get('prenom'),
        'telephone': request.session.get('telephone'),
        'date_nais': request.session.get('date_nais'),
        'civilite': request.session.get('civilite'),
        'role': request.session.get('role'),
        'email': request.session.get('email'),
        'genre': request.session.get('genre'),
        'mot_de_passe': request.session.get('mot_de_passe'),
        'confirmer_mot_de_passe': request.session.get('confirmer_mot_de_passe'),
        'imagesprofiles': request.session.get('imagesprofiles'),
        'cycle': request.session.get('cycle'),
        'filiere': request.session.get('filiere'),
        'niveaux': request.session.get('niveaux'),
    }

    if request.method == 'POST':
        form = DemandeForm(request.POST, user_data=user_data)
        if form.is_valid():
            print('allo11111111')
            form.save()
            messages.success(request, 'La demande a bien été envoyée')
            
            # Ajoutez ici toute logique supplémentaire après l'enregistrement de la demande
            return redirect('creer_demande')  # Remplacez 'nom_de_votre_vue_de_confirmation' par le nom de votre vue de confirmation
    else:
        form = DemandeForm(user_data=user_data)

    return render(request, 'pages/demande-pages.html', {'form': form, 'user_data': user_data})




def marquer_notification_lue(request, notification_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        try:
            notification = Notification.objects.get(id=notification_id)
            
        except Notification.DoesNotExist:
            return JsonResponse({'message': "La notification n'existe pas"}, status=404)

        if action == 'accepter':
            # Logique d'acceptation de la notification
            
            notification.is_accept = True
            notification.marquer_comme_lue()
            # Ajoutez ici la logique pour la nouvelle notification à l'expéditeur

            return JsonResponse({'message': 'Notification acceptée avec succès'})

        elif action == 'rejeter':
            # Logique de refus de la notification
            
            notification.is_refused = True
            notification.marquer_comme_lue()
            # Ajoutez ici la logique pour la nouvelle notification à l'expéditeur

            return JsonResponse({'message': 'Notification rejetée avec succès'})
        
        elif action == 'compris':
            # Logique de refus de la notification
            notification.marquer_comme_lue()
            # Ajoutez ici la logique pour la nouvelle notification à l'expéditeur

            return JsonResponse({'message': 'ok !'})

        else:
            return JsonResponse({'message': 'Action non reconnue'}, status=400)

    else:
        # Gérez le cas où la requête n'est pas de type POST
        return JsonResponse({'message': 'Méthode non autorisée'}, status=405)

    

def accepter_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.accepter_notification()

    # Enregistrez une nouvelle notification pour l'expéditeur
    contenu_exp = f"{notification.destinataire.user.last_name} {notification.destinataire.user.first_name} a accepté votre notification."
    nouvelle_notification_exp = Notification(destinataire=notification.expediteur, contenu=contenu_exp, date_creation=timezone.now())
    nouvelle_notification_exp.save()

    

    # Rediriger d'abord vers ispublied_memoire, puis vers marquer_notification_lue
    return redirect('marquer_notification_lue')


def refuser_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.refuser_notification()

    # Enregistrez une nouvelle notification pour l'expéditeur
    contenu_exp = f"{notification.destinataire.user.last_name} {notification.destinataire.user.first_name} a refusé votre notification."
    nouvelle_notification_exp = Notification(destinataire=notification.expediteur, contenu=contenu_exp, date_creation=timezone.now())
    nouvelle_notification_exp.save()

    return redirect('marquer_notification_lue')


@csrf_exempt  # Vous pouvez retirer cette décoration si CSRF n'est pas nécessaire
def creer_nouvelle_notification(request):
    if request.method == 'POST':
        expediteur_id = request.POST.get('expediteurId')
        destinataire_id = request.POST.get('destinataireId')
        message = request.POST.get('message')
        print(expediteur_id)
        print(destinataire_id)
        print(message)
        aujourdhui = date.today()

        try:
            expediteur = Etudiant.objects.get(id=expediteur_id)
            destinataire = Etudiant.objects.get(id=destinataire_id)
            
            nouvelle_notification = Notification(
                destinataire=destinataire,
                expediteur=expediteur,
                contenu=message,
                date_creation = aujourdhui,
            )
            print(nouvelle_notification)
            nouvelle_notification.save()

            return JsonResponse({'message': 'Nouvelle notification créée avec succès'})
        except Etudiant.DoesNotExist:
            return JsonResponse({'message': 'L\'expéditeur ou le destinataire n\'existe pas'}, status=404)
    else:
        return JsonResponse({'message': 'Méthode non autorisée'}, status=405)

# def registre_demande(request):
#     user_data = {key: request.session.get(key) for key in ['matricule', 'Identification' , 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}
#     print(user_data)
    
#     demandes = Demande.objects.all()
    
#     # Passer les données de l'utilisateur et les demandes au template
#     context = {'user_data': user_data, 'demandes': demandes}
#     return render(request, 'pages/registre_demande.html', context)


def registre_demande(request):
    user = request.user
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}

    if user_data.get('role') == 'Etudiant':
        demandes = Demande.objects.filter(etudiant__user=user)
    elif user_data.get('role') == 'CSS':
        demandes = Demande.objects.filter(identite_receptioniste__user=user)
    else:
        # Gérez le cas où le type d'utilisateur n'est pas défini correctement
        demandes = []

    context = {'user_data': user_data, 'demandes': demandes}
    return render(request, 'pages/registre_demande.html', context)




def imprimer_demande(request, demande_id):
    demande = get_object_or_404(Demande, id=demande_id)
    template_path = 'pages/imprimer_demande.html'
    context = {'demande': demande}
    # print(demande)

    # Créer une instance du modèle HTML
    template = get_template(template_path)
    html = template.render(context)

    # Créer un fichier PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="impression_demande_{demande_id}.pdf"'

    # Générer le PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Si le PDF a été généré avec succès, retournez la réponse
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    return response


def supprimer_demande(request, demande_id):
    demande = get_object_or_404(Demande, id=demande_id)
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}

    
    if request.method == 'POST':
        demande.delete()
        return redirect('registre_demande')

    context = {'demande': demande , 'user_data':user_data}
    return render(request, 'pages/supprimer_demande.html', context)


def modifier_demande(request, demande_id):
    demande = get_object_or_404(Demande, id=demande_id)
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}


    if request.method == 'POST':
        form = UpdateDemandeForm(request.POST, instance=demande)
        if form.is_valid():
            form.save()
            # Rediriger vers la page de détails de la demande ou une autre vue appropriée
            return redirect('registre_demande')
    else:
        form = UpdateDemandeForm(instance=demande)

    context = {'form': form, 'demande': demande , 'user_data':user_data}
    return render(request, 'pages/modifier_demande.html', context)



# def registre_bulletins(request):
#     user = request.user
#     user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}

#     if user_data.get('role') == 'Etudiant':
#         bulletins = Bulletin.objects.filter(etudiant__user=user, is_transfer_etudiant=True , is_signed=True)
#     else:
#         # Gérez le cas où le type d'utilisateur n'est pas défini correctement
#         bulletins = []

#     context = {'user_data': user_data, 'bulletins': bulletins}
#     return render(request, 'pages/support-bulletins.html', context)


# def registre_bulletins(request):

#     user = request.user
#     user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}

#     if user_data.get('role') == 'Etudiant':
#         # Récupérer les attestations de l'utilisateur depuis la table Attestation
#         bulletins = Bulletin.objects.filter(etudiant__user=user, is_transfer_etudiant=True, is_signed=True)
        
#         # Vérifier si certaines attestations ont été supprimées ou n'existent plus dans la table Attestation
#         for bulletin in bulletins:
#             if not Bulletin.objects.filter(id=bulletin.id).exists():
#                 # Récupérer les attestations archivées depuis la table Archives
#                 archive_bulletin = Archives_bulletins.objects.filter(etudiant__user=user, is_archived=True)

#                 print(archive_bulletin)
#                 # Ajouter les attestations archivées à la liste des attestations à afficher
#                 bulletins |= archive_bulletin
    
#     else:
#         # Gérez le cas où le type d'utilisateur n'est pas défini correctement
#         bulletins = []

#     context = {'user_data': user_data, 'bulletins': bulletins}
#     return render(request, 'pages/support-bulletins.html', context)


def registre_bulletins(request):
    user = request.user
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}

    if user_data.get('role') == 'Etudiant':
        # Récupérer les bulletins de l'utilisateur depuis la table Bulletin
        bulletins = Bulletin.objects.filter(etudiant__user=user, is_transfer_etudiant=True, is_signed=True)
        
        # Récupérer les bulletins archivés de l'utilisateur depuis la table Archives_bulletins
        archive_bulletins = Archives_bulletins.objects.filter(etudiant__user=user, is_archived=True)
        
        # Ajouter les bulletins archivés à la liste des bulletins à afficher
        bulletins = list(bulletins) + list(archive_bulletins)
    
    else:
        # Gérez le cas où le type d'utilisateur n'est pas défini correctement
        bulletins = []

    context = {'user_data': user_data, 'bulletins': bulletins}
    return render(request, 'pages/support-bulletins.html', context)


# def registre_attestations(request):
#     if not request.user.is_authenticated:
#         return redirect('SignInView') 
#     user = request.user
#     user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}

#     if user_data.get('role') == 'Etudiant':
#         attestations = Attestation.objects.filter(etudiant__user=user , is_transfer_etudiant=True , is_signed=True)
#     else:
#         # Gérez le cas où le type d'utilisateur n'est pas défini correctement
#         attestations = []

#     context = {'user_data': user_data, 'attestations': attestations}
#     return render(request, 'pages/support-attestations.html', context)



def registre_attestations(request):

    user = request.user
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}

    if user_data.get('role') == 'Etudiant':
        # Récupérer les attestations de l'utilisateur depuis la table Attestation
        attestations = Attestation.objects.filter(etudiant__user=user, is_transfer_etudiant=True, is_signed=True)
        
        # Vérifier si certaines attestations ont été supprimées ou n'existent plus dans la table Attestation
        for attestation in attestations:
            if not Attestation.objects.filter(id=attestation.id).exists():
                # Récupérer les attestations archivées depuis la table Archives
                archive = Archives.objects.filter(etudiant__user=user, is_archived=True)
                # Ajouter les attestations archivées à la liste des attestations à afficher
                attestations = list(attestations) + list(archive)

    
    else:
        # Gérez le cas où le type d'utilisateur n'est pas défini correctement
        attestations = []

    context = {'user_data': user_data, 'attestations': attestations}
    return render(request, 'pages/support-attestations.html', context)



def recherche_demande_de_etudiant(request):
    user = request.user
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}
    attestation_types = ['attestation_frequentation', 'attestation_reussite']  # Adjust these based on your actual types

    # Get the query and date parameters from the request
    query = request.GET.get('q')
    date_param = request.GET.get('date')

    # Start with the base queryset
    demandes = Demande.objects.filter(objet_demande__in=attestation_types)

    # Apply filters based on query and date parameters
    if query:
        demandes = demandes.filter(
            Q(objet_demande__icontains=query) 
        )

    if date_param:
        # Convert the date parameter to a date object
        date_obj = datetime.strptime(date_param, '%Y-%m-%d').date()
        demandes = demandes.filter(date_poste_demande=date_obj)

    # The rest of your logic for rendering the model to the view
    # ...

    context = {'demandes': demandes, 'user_data': user_data}
    return render(request, 'pages/registre_demande.html', context)

