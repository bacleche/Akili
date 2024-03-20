from django.shortcuts import render , redirect
from CSSAPP.data_models.css import CSS
from CSSAPP.data_models.documents import Attestation , Bulletin , Archives , Archives_bulletins
from EtudiantApp.data_models.demande import Demande
from EtudiantApp.data_models.notifications import Notification

from EtudiantApp.data_models.etudiant import Etudiant
from django.db.models import Q
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import logout
import csv
from django.core.paginator import Paginator

from datetime import date
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
# Create your views here.
from django.urls import reverse
from django.views.decorators.http import require_http_methods

#VUES POUR L'APP CSS

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('SignInView'))  # Redirige vers la page de connexion si l'utilisateur n'est pas connecté
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@require_http_methods(["GET"])
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
    writer.writerow([demande.date_poste_demande, demande.etudiant, demande.objet_demande , demande.genre , demande.telephone, demande.date_nais, demande.session_dut, demande.session_lic, demande.annee_academique, demande.mois, demande.filiere, demande.cycle,  demande.niveau])  # Remplacez avec les noms de vos champs

    # Vous pouvez ajouter plus de lignes si nécessaire

    return response


#csv pour toutes les demandes 
def generer_toutes_demandes_csv(request):
    # Récupérer toutes les demandes
    attestation_types_csv = ['attestation_frequentation', 'attestation_reussite']
    demandes = Demande.objects.filter(objet_demande__in=attestation_types_csv)

    # Créer une réponse avec le type MIME approprié pour CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="toutes_demandes.csv"'

    # Créer un écrivain CSV
    writer = csv.writer(response)

    # Écrire l'en-tête du fichier CSV
    writer.writerow(['Date d\emission', 'Etudiant', 'Objet' , 'Genre' , 'Telephone','Date de naissance' , 'Session DUT' , 'Session LIC' , 'Année Academique' , 'Mois' ,'Filière' , 'Cycle' , 'Niveau'])  # Remplacez avec les noms de vos champs

    # Écrire les données de chaque demande dans le fichier CSV
    for demande in demandes:
        writer.writerow([demande.date_poste_demande, demande.etudiant, demande.objet_demande , demande.genre , demande.telephone, demande.date_nais, demande.session_dut, demande.session_lic, demande.annee_academique, demande.mois, demande.filiere, demande.cycle,  demande.niveau])  # Remplacez avec les noms de vos champs

    return response




def generer_toutes_demandes_csv_bulletins(request):
    # Récupérer toutes les demandes
    attestation_types_csv = ['attestation_frequentation', 'attestation_reussite']
    demandes = Demande.objects.filter(objet_demande='bulletin')

    # Créer une réponse avec le type MIME approprié pour CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="toutes_demandes.csv"'

    # Créer un écrivain CSV
    writer = csv.writer(response)

    # Écrire l'en-tête du fichier CSV
    writer.writerow(['Date d\emission', 'Etudiant', 'Objet' , 'Genre' , 'Telephone','Date de naissance' , 'Session DUT' , 'Session LIC' , 'Année Academique' , 'Mois' ,'Filière' , 'Cycle' , 'Niveau'])  # Remplacez avec les noms de vos champs

    # Écrire les données de chaque demande dans le fichier CSV
    for demande in demandes:
        writer.writerow([demande.date_poste_demande, demande.etudiant, demande.objet_demande , demande.genre , demande.telephone, demande.date_nais, demande.session_dut, demande.session_lic, demande.annee_academique, demande.mois, demande.filiere, demande.cycle,  demande.niveau])  # Remplacez avec les noms de vos champs

    return response
#fin csv pour toutes demandes

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

    return render(request, 'pages/groupeslistes/liste_etudiants_licence_admin1.html', {'etudiants_licence': etudiants_licence , 'user_data': user_data})



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

    attestations = Attestation.objects.filter(is_signed=True, is_transfer_css=True)
    paginator = Paginator(attestations, 10)

    # Récupérer le numéro de la page à afficher, par défaut 1
    page_number = request.GET.get('page')
    
    # Récupérer les objets attestations pour la page donnée
    page_obj = paginator.get_page(page_number)

    return render(request, 'liste_documents/attestations.html', {'attestations': attestations , 'user_data': user_data, 'page_obj':page_obj})


def liste_bulletinsf(request):
    
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    bulletins = Bulletin.objects.filter(is_signed=True, is_transfer_css=True)
    print(bulletins)
    paginator = Paginator(bulletins, 10)

    # Récupérer le numéro de la page à afficher, par défaut 1
    page_number = request.GET.get('page')
    
    # Récupérer les objets attestations pour la page donnée
    page_obj = paginator.get_page(page_number) 
    return render(request, 'liste_documents/bulletins.html', {'bulletins': bulletins , 'user_data': user_data, 'page_obj': page_obj})






def recherche_Bulletins_css(request):
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

    return render(request, 'liste_documents/bulletins.html', {'bulletins': bulletins, 'user_data': user_data})




def recherche_attestation_css(request):
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

    return render(request, 'liste_documents/attestations.html', {'attestations': attestations, 'user_data': user_data})



def signaler_css_attestation_etudiant(request, attestation_id):
    attestation = Attestation.objects.get(id=attestation_id)
    attestation.is_transfer_etudiant = True
    # attestation.save()
    date_poste = date.today()

    titre_poste = "Attestation a été Signé"  
    contenu_notification = f"Votre : {titre_poste}, veuillez télécharger ou visualiser"
    date_creation = date_poste
    notification = Notification(destinataire=attestation.etudiant, expediteur_css=attestation.profiles_css ,  contenu=contenu_notification, date_creation=date_creation )
    print('est arrivé')
    notification.save()
    print(notification)
    attestation.save()
    print('fifi')

    return redirect('liste_Attestations')

def signaler_css_bulletin_etudiant(request, bulletin_id):
    bulletin = Bulletin.objects.get(id=bulletin_id)
    bulletin.is_transfer_etudiant = True
    date_poste = date.today()

    titre_poste = "Bulletin a été Signé"  
    contenu_notification = f"Votre : {titre_poste}, veuillez télécharger ou visualiser"
    date_creation = date_poste
    notification = Notification(destinataire=bulletin.etudiant, expediteur_css=bulletin.profiles_css ,  contenu=contenu_notification, date_creation=date_creation )
    print('est arrivé')
    notification.save()
    print(notification)
    bulletin.save()
    print('fifi')
    return redirect('liste_bulletinsf')




#--------impression-document-------------------



def imprimer_attestations_css_doc(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    # Récupérer toutes les attestations à imprimer
    attestations = Attestation.objects.all()  # Assurez-vous de remplacer VotreModele par votre propre modèle
    datey = date.today()
    # Charger le template HTML
    template_path = 'pages/imprimer_attestation_css_doc.html'
    template = get_template(template_path)
    
    # Remplir le template avec les données des attestations
    context = {'attestations': attestations, 'user_data': user_data , 'datey':datey}
    html = template.render(context)

    # Générer le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="liste_attestations_doc.pdf"'
    
    # Convertir le HTML en PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Vérifier si la conversion s'est bien déroulée
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    
    return response



def imprimer_bulletins_css_doc(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    # Récupérer toutes les attestations à imprimer
    bulletins = Bulletin.objects.all()  # Assurez-vous de remplacer VotreModele par votre propre modèle
    print(bulletins)
    datey = date.today()
    # Charger le template HTML
    template_path = 'pages/imprimer_bulletins_css_doc.html'
    template = get_template(template_path)
    
    # Remplir le template avec les données des attestations
    context = {'bulletins': bulletins, 'user_data': user_data , 'datey':datey}
    html = template.render(context)

    # Générer le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="liste_bulletins_doc.pdf"'
    
    # Convertir le HTML en PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Vérifier si la conversion s'est bien déroulée
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    
    return response

#-------------FIn



def archive_documents_attestation(request):
    # Récupérer toutes les attestations non archivées
    attestations = Attestation.objects.filter(is_archived=False)
    
    # Archiver chaque attestation
    for attestation in attestations:
        archive = Archives(etudiant=attestation.etudiant, file=attestation.file)
        archive.save()
        attestation.is_archived = True
        attestation.save()
    
    # Ajouter un message de confirmation
    messages.success(request, "Toutes les attestations ont été archivées avec succès.")
    
    return redirect('liste_Attestations')



def archive_documents_bulletins(request):
    # Récupérer toutes les attestations non archivées
    bulletins = Bulletin.objects.filter(is_archived=False)
    
    # Archiver chaque attestation
    for bulletin in bulletins:
        archive = Archives_bulletins(etudiant=bulletin.etudiant, file=bulletin.file)
        archive.save()
        bulletin.is_archived = True
        bulletin.save()
    
    # Ajouter un message de confirmation
    messages.success(request, "Toutes les attestations ont été archivées avec succès.")
    
    return redirect('liste_bulletinsf')



def supprimer_bulletin_css(request):

    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}

    bulletin = Bulletin.objects.all().delete()
    context = {'user_data':user_data}
    return redirect('liste_bulletinsf')



def supprimer_attestation_css(request):

    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}

    attestations = Attestation.objects.all().delete()
    context = {'user_data':user_data}
    return redirect('liste_Attestations')




def supprimer_demandes_attestation_sup(request):
    # Récupérer toutes les demandes avec l'objet "bulletin"
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}

    attestation_types = ['attestation_frequentation', 'attestation_reussite']  # Adjust these based on your actual types

    demandes_attestation = Demande.objects.filter(objet_demande__in=attestation_types)

    # Afficher une page de confirmation avec la liste des demandes à supprimer
    return render(request, 'pages/confirmer_suppression_demandes_attestation.html', {'demandes_attestation': demandes_attestation, 'user_data': user_data})

def confirmer_suppression_demandes_attestation(request):
    if request.method == 'POST':
        # Supprimer toutes les demandes avec l'objet "bulletin"
        attestation_types = ['attestation_frequentation', 'attestation_reussite']  # Adjust these based on your actual types
        
        Demande.objects.filter(objet_demande=attestation_types).delete()
        
        # Rediriger vers une autre vue après la suppression
        return redirect('list_demandes')
    else:
        # Si la méthode HTTP n'est pas POST, rediriger vers la page de confirmation
        return redirect('supprimer_demandes_attestation_sup')
    


def supprimer_demandes_bulletin_sup(request):
    # Récupérer toutes les demandes avec l'objet "bulletin"
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe', 'confirmer_mot_de_passe', 'imagesprofiles']}
    demandes_bulletin = Demande.objects.filter(objet_demande='bulletin')

    # Afficher une page de confirmation avec la liste des demandes à supprimer
    return render(request, 'pages/confirmer_suppression_demandes_bulletin.html', {'demandes_bulletin': demandes_bulletin, 'user_data': user_data})

def confirmer_suppression_demandes_bulletin(request):
    if request.method == 'POST':
        # Supprimer toutes les demandes avec l'objet "bulletin"
        Demande.objects.filter(objet_demande='bulletin').delete()
        
        # Rediriger vers une autre vue après la suppression
        return redirect('list_bulletin_demandes')
    else:
        # Si la méthode HTTP n'est pas POST, rediriger vers la page de confirmation
        return redirect('supprimer_demandes_bulletin')






def imprimer_toutes_les_demandes_bulletin(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    # Filtrer les demandes dont l'objet est "bulletin"
    demandes = Demande.objects.filter(objet_demande='bulletin')
    datey = date.today()

    # Chemin du template HTML à utiliser pour générer le PDF
    template_path = 'pages/imprimer_toutes_bulletins.html'

    # Initialiser une liste pour stocker les PDF générés
    pdfs = []

    # Pour chaque demande, générer le PDF et l'ajouter à la liste des PDFs
    for demande in demandes:
        context = {'demandes': demandes, 'user_data': user_data, 'datey': datey}
        template = get_template(template_path)
        html = template.render(context)

        # Créer un fichier PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="impression_demande_{demande}.pdf"'

        # Générer le PDF
        pisa_status = pisa.CreatePDF(html, dest=response)
        
        # Si le PDF a été généré avec succès, ajoutez-le à la liste des PDFs
        if not pisa_status.err:
            pdfs.append(response)

    # Concaténer tous les PDFs en une seule réponse
    final_pdf = b''.join([pdf.content for pdf in pdfs])
    response = HttpResponse(final_pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="impression_demandes_bulletin.pdf"'
    return response



def imprimer_toutes_les_demandes_attestations_dem(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}
    attestation_types = ['attestation_frequentation', 'attestation_reussite']  # Adjust these based on your actual types

    # Filtrer les demandes dont l'objet est "bulletin"
    demandes = Demande.objects.filter(objet_demande__in=attestation_types)
    datey = date.today()

    # Chemin du template HTML à utiliser pour générer le PDF
    template_path = 'pages/imprimer_toutes_attestations_dem.html'

    # Initialiser une liste pour stocker les PDF générés
    pdfs = []

    # Pour chaque demande, générer le PDF et l'ajouter à la liste des PDFs
    for demande in demandes:
        context = {'demandes': demandes, 'user_data': user_data, 'datey': datey}
        template = get_template(template_path)
        html = template.render(context)

        # Créer un fichier PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="impression_demande_attestation_{demande}.pdf"'

        # Générer le PDF
        pisa_status = pisa.CreatePDF(html, dest=response)
        
        # Si le PDF a été généré avec succès, ajoutez-le à la liste des PDFs
        if not pisa_status.err:
            pdfs.append(response)

    # Concaténer tous les PDFs en une seule réponse
    final_pdf = b''.join([pdf.content for pdf in pdfs])
    response = HttpResponse(final_pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="impression_demandes_bulletin.pdf"'
    return response




def custom_logout(request):
    logout(request)
    return redirect('SignInView')  