from django.shortcuts import render , redirect
from CSSAPP.data_models.css import CSS
from EtudiantApp.data_models.demande import Demande

from django.contrib import messages
from django.contrib.auth import logout

from django.shortcuts import get_object_or_404

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
        demandes = Demande.objects.filter(identite_receptioniste__user=user, objet_demande='bulletin')
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


def custom_logout(request):
    logout(request)
    return redirect('SignInView')