from django.shortcuts import render , redirect
from CSSAPP.data_models.css import CSS

from django.contrib.auth import logout


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

def mis_a_jour(request):
    # Récupérez l'utilisateur actuel (CSS dans ce cas)
    user = CSS.objects.get(matricule=request.session.get('matricule'))
    
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

        return redirect('Profiles_css')  # Redirigez vers la page de détails après la modification

    return render(request, 'pages/profile-modify.html', {'user': user})


def custom_logout(request):
    logout(request)
    return redirect('SignInView')