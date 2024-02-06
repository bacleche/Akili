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

def cssWork(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}
    return render(request, 'pages/index-css.html', user_data)

def Profiles_css(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}
    return render(request, 'pages/profile-css.html', user_data)


def profile_details(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}
    user_data['civilite_choices'] = CSS._meta.get_field('civilite').choices
    return render(request, 'pages/profile-modify.html', user_data)

def mis_a_jour_css(request):
    # Récupérez l'utilisateur actuel (CSS dans ce cas)
    user = CSS.objects.get(matricule=request.session.get('matricule'))
    
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
                return redirect('update_profile')
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

            return redirect('Profiles_css')  # Redirigez vers la page de détails après la modification

        else:
            print('ddddddeuueueueue')
            messages.error(request, 'Les mots de passe doivent etre identiques')
            return redirect('update_profile')

    return render(request, 'pages/profile-modify.html', {'user': user})


def list_demandes(request):
    user = request.user
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}

    attestation_types = ['attestation_frequentation', 'attestation_reussite']  # Adjust these based on your actual types

    if user_data.get('role') == 'Etudiant':
        demandes = Demande.objects.filter(etudiant__user=user)
    elif user_data.get('role') == 'CSS':
        demandes = Demande.objects.filter(identite_receptioniste__user=user , objet_demande__in=attestation_types)
        print('oui')
        print(demandes)
    else:
        # Gérez le cas où le type d'utilisateur n'est pas défini correctement
        demandes = []

    context = {'user_data': user_data, 'demandes': demandes}
    return render(request, 'pages/list_attestations.html', context)



def list_bulletin_demandes(request):
    user = request.user
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}
  
    if user_data.get('role') == 'Etudiant':
        demandes = Demande.objects.filter(etudiant__user=user)
    elif user_data.get('role') == 'CSS':
        demandes = Demande.objects.filter(identite_receptioniste__user=user , objet_demande='bulletin')
        print('oui')
        print((user_data.get('role')))
        print(demandes)


    else:
        demandes = []

    context = {'user_data': user_data, 'demandes': demandes}
    return render(request, 'pages/list_bulletins.html', context)

def imprimer_demande_css(request, demande_id):
    demande = get_object_or_404(Demande, id=demande_id)
    template_path = 'pages/imprimer_demande_css.html'
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



def generer_fichier_csv(request, demande_id):
    demande = get_object_or_404(Demande, id=demande_id)

    # Créer une réponse avec le type MIME approprié pour CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="donnees_demande_{demande_id}.csv"'

    # Créer un écrivain CSV
    writer = csv.writer(response)

    # Écrire l'en-tête du fichier CSV
    writer.writerow(['Date d\emission', 'Etudiant', 'Objet' , 'Genre' , 'Telephone','Date de naissance' , 'Session DUT' , 'Session LIC' , 'Année Academique' , 'Mois' ,'Filière' , 'Cycle' , 'Niveau'])  # Remplacez avec les noms de vos champs

    # Écrire les données de la demande dans le fichier CSV
    writer.writerow([demande.date_poste_demande, demande.etudiant, demande.objet_demande , demande.genre , demande.telephone, demande.date_nais, demande.session_dut, demande.session_lic, demande.annee_academique, demande.mois, demande.filiere, demande.niveau])  # Remplacez avec les noms de vos champs

    # Vous pouvez ajouter plus de lignes si nécessaire

    return response



# def recherche_demande_par_etudiant(request):
#     user = request.user
#     user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}
    
#     if 'q' in request.GET:
#         query = request.GET['q']
#         print(query)
#         demandes = Demande.objects.filter(objet_demande='bulletin', etudiant__user__first_name__icontains=query) | \
#                    Demande.objects.filter(objet_demande='bulletin', etudiant__user__last_name__icontains=query) | \
#                    Demande.objects.filter(objet_demande='bulletin', etudiant__user__username__icontains=query) 
#     else:
#         demandes = Demande.objects.filter(objet_demande='bulletin')

#     context = {'demandes': demandes, 'user_data': user_data}
#     return render(request, 'pages/list_bulletins.html', context)

def recherche_demande_par_etudiant(request):
    user = request.user
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}
    
    # Get the query and date parameters from the request
    query = request.GET.get('q')
    date_param = request.GET.get('date')

    # Start with the base queryset
    demandes = Demande.objects.filter(objet_demande='bulletin')

    # Apply filters based on query and date parameters
    if query:
        demandes = demandes.filter(
            Q(etudiant__user__first_name__icontains=query) |
            Q(etudiant__user__last_name__icontains=query) |
            Q(etudiant__user__username__icontains=query)
        )

    if date_param:
        # Convert the date parameter to a date object
        date_obj = datetime.strptime(date_param, '%Y-%m-%d').date()
        demandes = demandes.filter(date_poste_demande=date_obj)

    context = {'demandes': demandes, 'user_data': user_data}
    return render(request, 'pages/list_bulletins.html', context)






# def recherche_demande_par_etudiant_attestations(request):
#     user = request.user
#     user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}
#     attestation_types = ['attestation_frequentation', 'attestation_reussite']  # Adjust these based on your actual types
#     if 'q' in request.GET:
#         query = request.GET['q']
#         print(query)
#         demandes = Demande.objects.filter(objet_demande__in=attestation_types, etudiant__user__first_name__icontains=query) | \
#                    Demande.objects.filter(objet_demande__in=attestation_types ,etudiant__user__last_name__icontains=query) | \
#                    Demande.objects.filter(objet_demande__in=attestation_types, etudiant__user__username__icontains=query) 
#     else:
#         demandes = Demande.objects.filter(objet_demande__in=attestation_types)

#     context = {'demandes': demandes, 'user_data': user_data}
#     return render(request, 'pages/list_attestations.html', context)

def recherche_demande_par_etudiant_attestations(request):
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
            Q(etudiant__user__first_name__icontains=query) |
            Q(etudiant__user__last_name__icontains=query) |
            Q(etudiant__user__username__icontains=query)
        )

    if date_param:
        # Convert the date parameter to a date object
        date_obj = datetime.strptime(date_param, '%Y-%m-%d').date()
        demandes = demandes.filter(date_poste_demande=date_obj)

    # The rest of your logic for rendering the model to the view
    # ...

    context = {'demandes': demandes, 'user_data': user_data}
    return render(request, 'pages/list_attestations.html', context)


def liste_etudiant_classifications(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}
    return render(request, 'pages/liste_etudiant_classifications.html', user_data)



"""
Debut  Fonction liste ------------------------------------------------------------------ //---------------------
"""


#-----------------LICENCE INFORMATIQUE- --------------------------------------



def liste_etudiants_licence(request):
    
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    etudiants_licence = Etudiant.objects.filter(cycle='licence', niveaux='licence1', filiere='informatique', statut='En Fréquentation')

    return render(request, 'pages/groupeslistes/liste_licence1.html', {'etudiants_licence': etudiants_licence , 'user_data': user_data})



def liste_etudiants_licence_info2(request):
    
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    etudiants_licence = Etudiant.objects.filter(cycle='licence', niveaux='licence2',  filiere='informatique', statut='En Fréquentation')

    return render(request, 'pages/groupeslistes/liste_etudiant_licence2_info.html', {'etudiants_licence': etudiants_licence , 'user_data': user_data})


def liste_etudiants_licence_info3(request):
    
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    etudiants_licence = Etudiant.objects.filter(cycle='licence', niveaux='licence3' , filiere='informatique',  statut='En Fréquentation')

    return render(request, 'pages/groupeslistes/liste_etudiant_licence2_info.html', {'etudiants_licence': etudiants_licence , 'user_data': user_data})

#-----------------Fin LICENCE INFORMATIQUE- --------------------------------------


#-----------------DUT INFORMATIQUE- --------------------------------------

def liste_etudiants_dut_info1(request):
    
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    etudiants_dut = Etudiant.objects.filter(cycle='dut', niveaux='dut1' , filiere='informatique', statut='En Fréquentation')

    return render(request, 'pages/groupeslistes/liste_etudiant_info_dut1.html', {'etudiants_dut': etudiants_dut , 'user_data': user_data})


def liste_etudiants_dut_info2(request):
    
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    etudiants_dut = Etudiant.objects.filter(cycle='dut', niveaux='dut2' ,  filiere='informatique', statut='En Fréquentation')

    return render(request, 'pages/groupeslistes/liste_etudiant_info_dut2.html', {'etudiants_dut': etudiants_dut , 'user_data': user_data})

#-----------------Fin DUT INFORMATIQUE- --------------------------------------

#-----------------DUT ADMINISTRATION- --------------------------------------

def liste_etudiants_administration_dut1(request):
    
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    etudiants_dut = Etudiant.objects.filter(cycle='dut', niveaux='dut2' ,  filiere='administration', statut='En Fréquentation')

    return render(request, 'pages/groupeslistes/liste_etudiant_administration_dut1.html', {'etudiants_dut': etudiants_dut , 'user_data': user_data})



def liste_etudiants_administration_dut2(request):
    
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    etudiants_dut = Etudiant.objects.filter(cycle='dut', niveaux='dut2' ,  filiere='administration', statut='En Fréquentation')

    return render(request, 'pages/groupeslistes/liste_etudiant_administration_dut2.html', {'etudiants_dut': etudiants_dut , 'user_data': user_data})



#-----------------FIn DUT ADMINISTRATION- --------------------------------------

#-----------------LICENCE ADMINISTRATION- --------------------------------------


def liste_etudiants_licence_admin1(request):
    
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    etudiants_licence = Etudiant.objects.filter(cycle='licence', niveaux='licence1', filiere='administration', statut='En Fréquentation')

    return render(request, 'pages/groupeslistes/liste_licence_admin1.html', {'etudiants_licence': etudiants_licence , 'user_data': user_data})



def liste_etudiants_licence_admin2(request):
    
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    etudiants_licence = Etudiant.objects.filter(cycle='licence', niveaux='licence2',  filiere='administration', statut='En Fréquentation')

    return render(request, 'pages/groupeslistes/liste_etudiant_licence_admin2.html', {'etudiants_licence': etudiants_licence , 'user_data': user_data})


def liste_etudiants_licence_admin3(request):
    
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    etudiants_licence = Etudiant.objects.filter(cycle='licence', niveaux='licence3' , filiere='administration',  statut='En Fréquentation')

    return render(request, 'pages/groupeslistes/liste_etudiant_licence_admin3.html', {'etudiants_licence': etudiants_licence , 'user_data': user_data})



#-----------------LICENCE ADMINISTRATION- --------------------------------------



"""
FIn Fonction liste ------------------------------------------------------------------ //---------------------
"""



def supprimer_demande_css_bulletin(request, demande_id):
    demande = get_object_or_404(Demande, id=demande_id)
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}

    
    if request.method == 'POST':
        demande.delete()
        return redirect('list_bulletin_demandes')

    context = {'demande': demande , 'user_data':user_data}
    return render(request, 'pages/supprimer_demande_css.html', context)


def supprimer_demande_css_attestation(request, demande_id):
    demande = get_object_or_404(Demande, id=demande_id)
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}

    
    if request.method == 'POST':
        demande.delete()
        return redirect('list_demandes')

    context = {'demande': demande , 'user_data':user_data}
    return render(request, 'pages/supprimer_demande_css.html', context)



def update_etudiant_statut(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)

    if request.method == 'POST':
        nouveau_statut = request.POST.get('statut', 'Ancien étudiant')
        etudiant.statut = nouveau_statut
        etudiant.save()

        if etudiant.statut == 'Ancien étudiant':
            messages.success(request, f'Le statut de l\'étudiant {etudiant.user.last_name} {etudiant.user.first_name} a été mis à jour avec succès.')
            return redirect('liste_etudiants_licence')
        else:
            messages.success(request, f'Le statut de l\'étudiant {etudiant.user.last_name} {etudiant.user.first_name} a échoué.')
            return redirect('liste_etudiant_classifications')

    return JsonResponse({'success': False, 'error_message': 'Méthode non autorisée'})



def changer_etat_demande_attestion(request, demande_id, action):
    demande = get_object_or_404(Demande, id=demande_id)

    if action == 'acceptee':
        demande.etat = 'Acceptée'
        demande.date_de_fin_treatment = date.today()

    elif action == 'traitement':
        demande.etat = 'En cours de traitement'
        demande.date_de_mise_en_traitement = date.today()
    elif action == 'refusee':
        demande.etat = 'Refusée'
        demande.date_refus = date.today()
    elif action == 'terminee':
        demande.etat = 'Terminée'
        demande.date_termine = date.today()
    # Ajoutez d'autres co
    demande.save()
    
    # Redirigez l'utilisateur vers la page précédente ou une autre page appropriée
    return redirect('list_demandes')



def changer_etat_demande_bulletin(request, demande_id, action):
    demande = get_object_or_404(Demande, id=demande_id)

    if action == 'acceptee':
        demande.etat = 'Acceptée'
        demande.date_de_fin_treatment = date.today()

    elif action == 'traitement':
        demande.etat = 'En cours de traitement'
        demande.date_de_mise_en_traitement = date.today()
    elif action == 'refusee':
        demande.etat = 'Refusée'
        demande.date_refus = date.today()
    elif action == 'terminee':
        demande.etat = 'Terminée'
        demande.date_termine = date.today()
    # Ajoutez d'autres conditions pour d'autres actions si nécessaire

    demande.save()
    
    # Redirigez l'utilisateur vers la page précédente ou une autre page appropriée
    return redirect('list_bulletin_demandes')


# def historique_demandes(request):
#     user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}

#     # Récupérez toutes les demandes depuis la base de données (ajustez selon votre modèle)
#     demandes_en_attente = Demande.objects.filter(etat='En attente')
#     demandes_en_cours = Demande.objects.filter(etat='En cours de traitement')
#     demandes_terminees = Demande.objects.filter(etat='Terminée')
#     demandes_refusees = Demande.objects.filter(etat='Refusée')

#     # Passez les données au modèle
#     context = {
#         'historique_demandes': [
#             ('En attente', demandes_en_attente),
#             ('En cours de traitement', demandes_en_cours),
#             ('Terminée', demandes_terminees),
#             ('Refusée', demandes_refusees),
#         ],
#         'user_data': user_data,
#     }

    

#     # Renvoyez la vue avec les données
#     return render(request, 'pages/historiques_demandes.html', context)




# views.py
def historique_demandes(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}

    # Récupérez toutes les demandes depuis la base de données (ajustez selon votre modèle)
    demandes_en_attente = Demande.objects.filter(etat='En attente')
    demandes_en_cours = Demande.objects.filter(etat='En cours de traitement')
    demandes_acceptee = Demande.objects.filter(etat='Acceptée')
    demandes_terminees = Demande.objects.filter(etat='Terminée')
    demandes_refusees = Demande.objects.filter(etat='Refusée')

    # Calculez le nombre total de demandes pour chaque état
    total_attente = demandes_en_attente.count()
    total_en_cours = demandes_en_cours.count()
    total_acceptee = demandes_acceptee.count()  # Supposez que les demandes acceptées sont marquées comme 'Terminée'
    total_refusee = demandes_refusees.count()
    total_terminee = demandes_terminees.count()

    # Passez les données au modèle
    context = {
        'historique_demandes': [
            ('En attente', demandes_en_attente),
            ('En cours de traitement', demandes_en_cours),
            ('Acceptée', demandes_acceptee),
            ('Terminée', demandes_terminees),
            ('Refusée', demandes_refusees),
        ],
        'user_data': user_data,
        'totals': {
            'total_attente': total_attente,
            'total_en_cours': total_en_cours,
            'total_acceptee': total_acceptee,
            'total_refusee': total_refusee,
            'total_terminee': total_terminee,
        },
    }

    # Renvoyez la vue avec les données
    return render(request, 'pages/historiques_demandes.html', context)



def stat_morris(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}
    
    demandes_acceptees = Demande.objects.filter(etat='Acceptée').count()
    demandes_en_attente = Demande.objects.filter(etat='En attente').count()
    demandes_terminées = Demande.objects.filter(etat='Terminée').count()
    demandes_en_cours = Demande.objects.filter(etat='En cours de traitement').count()
    demandes_refusees = Demande.objects.filter(etat='Refusée').count()

    print(demandes_acceptees)

    # Ajout des statistiques au contexte de rendu
    return render(request, 'pages/statistiques-morris.html', {
        **user_data,  # Ajoute les données de l'utilisateur au contexte
        'demandes_acceptees': demandes_acceptees,
        'demandes_en_attente': demandes_en_attente,
        'demandes_terminées': demandes_terminées,
        'demandes_en_cours': demandes_en_cours,
        'demandes_refusees': demandes_refusees,
    })


def taux_etudiants(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    licence_info_taux = Etudiant.objects.filter(cycle__startswith='licence', filiere='informatique').count()
    licence_admin_taux = Etudiant.objects.filter(cycle__startswith='licence', filiere='administration').count()
    dut_info_taux = Etudiant.objects.filter(cycle__startswith='dut', filiere='informatique').count()
    dut_admin_taux = Etudiant.objects.filter(cycle__startswith='dut', filiere='administration').count()
    
    return render(request, 'pages/taux-etudiants.html', {
        **user_data,  # Ajoute les données de l'utilisateur au contexte
        'licence_info_taux': licence_info_taux,
        'licence_admin_taux': licence_admin_taux,
        'dut_info_taux': dut_info_taux,
        'dut_admin_taux': dut_admin_taux,
    })

   

# def create_document(request, etudiant_id):
#     etudiant = Etudiant.objects.get(id=etudiant_id)
    


#     if request.method == 'POST':
#         type_attestation = request.POST.get('type_attestation')
#         document = request.POST.get('document')
#         date_regis = date.today()
#         docs = request.FILES.get('docs')
#         if document == 'attestation':
#             # Créer une nouvelle attestation pour l'étudiant
#             Attestation.objects.create(
#                 etudiant=etudiant,
#                 types_attestation = type_attestation,
#                 date_register = date_regis,
#                 file = docs,
#                 # Ajoutez d'autres champs spécifiques à l'attestation ici...
#             )
#         elif document == 'bulletin':
#             # Créer un nouveau bulletin pour l'étudiant
#             Bulletin.objects.create(
#                 etudiant=etudiant,
#                 date_register = date_regis,
#                 file = docs,
#                 # Ajoutez d'autres champs spécifiques au bulletin ici...
#             )


#     return render(request, 'pages/create_document.html', {'etudiant': etudiant})



def liste_Attestations(request):
    
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    attestations = Attestation.objects.all()

    return render(request, 'liste_documents/attestations.html', {'attestations': attestations , 'user_data': user_data})


def liste_bulletinsf(request):
    
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    bulletins = Bulletin.objects.all()

    return render(request, 'liste_documents/bulletins.html', {'bulletins': bulletins , 'user_data': user_data})




def custom_logout(request):
    logout(request)
    return redirect('SignInView')