from django.shortcuts import render , redirect
from EtudiantApp.data_models.etudiant import Etudiant
from .forms import *
from django.contrib import messages
from Utilisateur.data_models.utilisateur import Utilisateur
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from EtudiantApp.data_models.notifications import Notification
from django.shortcuts import HttpResponse
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt


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
        user.nom = request.POST.get('nom')
        user.prenom = request.POST.get('prenom')
        user.telephone = request.POST.get('phone')
        user.date_nais = request.POST.get('date')
        user.civilite = request.POST.get('civilite')
        user.role = request.POST.get('surname')  # Assurez-vous que le nom du champ correspond
        user.email = request.POST.get('email')
        user.role = request.POST.get('role')
        user.date_nais = request.POST.get('date_nais')
        user.mot_de_passe = request.POST.get('password')
        user.confirmer_mot_de_passe = request.POST.get('password_conf')

        # Gérez l'image de profil
        if 'new_profile_image' in request.FILES:
            image = request.FILES['new_profile_image']
            # Enregistrez l'image avec un nouveau nom pour éviter les collisions
            image_name = f"profile_image_{user.matricule}.{image.name.split('.')[-1]}"
            user.imagesprofiles.save(image_name, image)

        # Sauvegardez les modifications
        user.save()

        # Mettez à jour les données de la session avec les nouvelles valeurs
        request.session['nom'] = user.nom
        request.session['prenom'] = user.prenom
        request.session['telephone'] = user.telephone
        request.session['date_nais'] = user.date_nais
        request.session['civilite'] = user.civilite
        request.session['role'] = user.role
        request.session['email'] = user.email
        request.session['genre'] = user.genre
        request.session['mot_de_passe'] = user.mot_de_passe
        request.session['confirmer_de_passe'] = user.confirmer_mot_de_passe
        request.session['imagesprofiles'] = user.imagesprofiles.url

        return redirect('Profiles_etudiant')  # Redirigez vers la page de détails après la modification

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
            form.save()
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
            notification.marquer_comme_lue()
            # Ajoutez ici la logique pour la nouvelle notification à l'expéditeur

            return JsonResponse({'message': 'Notification acceptée avec succès'})

        elif action == 'rejeter':
            # Logique de refus de la notification
            notification.marquer_comme_lue()
            # Ajoutez ici la logique pour la nouvelle notification à l'expéditeur

            return JsonResponse({'message': 'Notification rejetée avec succès'})

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

        try:
            expediteur = Etudiant.objects.get(id=expediteur_id)
            destinataire = Etudiant.objects.get(id=destinataire_id)
            
            nouvelle_notification = Notification(
                destinataire=destinataire,
                expediteur=expediteur,
                contenu=message,
            )
            print(nouvelle_notification)
            nouvelle_notification.save()

            return JsonResponse({'message': 'Nouvelle notification créée avec succès'})
        except Etudiant.DoesNotExist:
            return JsonResponse({'message': 'L\'expéditeur ou le destinataire n\'existe pas'}, status=404)
    else:
        return JsonResponse({'message': 'Méthode non autorisée'}, status=405)
