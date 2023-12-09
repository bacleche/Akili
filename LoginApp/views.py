from django.shortcuts import render, redirect
from EtudiantApp.data_models.etudiant import Etudiant
from CSSAPP.data_models.css import CSS
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from Utilisateur.data_models.utilisateur import Utilisateur
from django.contrib.auth import authenticate, login


# def sign_in(request):
#     error_message = None  
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('your_pass')
#         etudiant = Etudiant.objects.filter(email=email).first()
#         print(etudiant)
#         css = CSS.objects.filter(email=email).first()
#         print(css)
#         if etudiant and etudiant.mot_de_passe == password:
#                 request.session['matricule'] = etudiant.matricule
#                 request.session['Identification'] = etudiant.Identification
#                 request.session['nom'] = etudiant.nom
#                 request.session['prenom'] = etudiant.prenom
#                 request.session['civilite'] = etudiant.civilite
#                 request.session['email'] = etudiant.email
#                 request.session['role'] = etudiant.role
#                 request.session['genre'] = etudiant.genre
#                 request.session['telephone'] = etudiant.telephone
#                 request.session['date_nais'] = etudiant.date_nais.strftime('%Y-%m-%d')
#                 request.session['mot_de_passe'] = etudiant.mot_de_passe
#                 request.session['confirmer_mot_de_passe'] = etudiant.confirmer_mot_de_passe
#                 request.session['imagesprofiles'] = etudiant.imagesprofiles.url 
#                 request.session['cycle'] = etudiant.cycle
#                 request.session['filiere'] = etudiant.filiere
#                 request.session['niveaux'] = etudiant.niveaux

#                 return redirect('student_space')
        
#         elif css and css.mot_de_passe == password:
#                 request.session['matricule'] = css.matricule
#                 request.session['nom'] = css.nom
#                 request.session['prenom'] = css.prenom
#                 request.session['civilite'] = css.civilite
#                 request.session['email'] = css.email
#                 request.session['role'] = css.role 
#                 request.session['genre'] = css.genre 
#                 request.session['telephone'] = css.telephone 
#                 request.session['date_nais'] = css.date_nais.strftime('%Y-%m-%d')
#                 request.session['mot_de_passe'] = css.mot_de_passe
#                 request.session['confirmer_mot_de_passe'] = css.confirmer_mot_de_passe
#                 request.session['imagesprofiles'] = css.imagesprofiles.url 
#                 return redirect('cssWork')
#         else : 
#             print('rate')
#         error_message = "L'authentification a échoué. Veuillez vérifier vos identifiants."

#     return render(request, 'login.html', {'error_message': error_message})


# def sign_in(request):
#     error_message = None

#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('your_pass')

#         try:
#             # Essayez de récupérer un étudiant ou un CSS avec l'email donné
#             utilisateur = Etudiant.objects.get(email=email)
#         except Etudiant.DoesNotExist:
#             try:
#                 utilisateur = CSS.objects.get(email=email)
#             except CSS.DoesNotExist:
#                 # Utilisateur non trouvé
#                 error_message = "Email et/ou Mot de passe Incorrect ! réessayez."
#                 messages.error(request, error_message)
#                 return render(request, 'login.html', {'error_message': error_message})

#         # Vérifiez le mot de passe et redirigez en conséquence
#         if utilisateur.password == password:
#             if isinstance(utilisateur, Etudiant):
#                 request.session['matricule'] = utilisateur.matricule
#                 request.session['Identification'] = utilisateur.Identification
#                 request.session['nom'] = utilisateur.nom
#                 request.session['prenom'] = utilisateur.prenom
#                 request.session['telephone'] = utilisateur.telephone
#                 request.session['date_nais'] = utilisateur.date_nais.strftime('%Y-%m-%d')
#                 request.session['civilite'] = utilisateur.civilite
#                 request.session['role'] = utilisateur.role
#                 request.session['email'] = utilisateur.email
#                 request.session['genre'] = utilisateur.genre
#                 request.session['mot_de_passe'] = utilisateur.password
#                 request.session['imagesprofiles'] = utilisateur.imagesprofiles.url
#                 request.session['cycle'] = utilisateur.cycle
#                 request.session['filiere'] = utilisateur.filiere
#                 request.session['niveaux'] = utilisateur.niveaux
               
#                 return redirect('student_space')
#             elif isinstance(utilisateur, CSS):
#                 # Ajoutez les attributs de session pour CSS si nécessaire
#                 return redirect('cssWork')
#         else:
#             error_message = "Email et/ou Mot de passe Incorrect ! réessayez."

#     return render(request, 'login.html', {'error_message': error_message})


def sign_in(request):
    error_message = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('your_pass')

        try:
            # Essayez de récupérer un étudiant ou un CSS avec l'email donné
            utilisateur = Etudiant.objects.get(user__email=email)
        except Etudiant.DoesNotExist:
            try:
                utilisateur = CSS.objects.get(user__email=email)
            except CSS.DoesNotExist:
                # Utilisateur non trouvé
                error_message = "Email et/ou Mot de passe Incorrect ! réessayez."
                messages.error(request, error_message)
                return render(request, 'login.html', {'error_message': error_message})

        # Vérifiez le mot de passe en utilisant la méthode check_password
        if utilisateur.user.check_password(password):
            # Authentification réussie, connectez l'utilisateur
            login(request, utilisateur.user)

            if isinstance(utilisateur, Etudiant):
                # Redirigez l'utilisateur en fonction de son rôle
                request.session['matricule'] = utilisateur.matricule
                request.session['Identification'] = utilisateur.Identification
                request.session['nom'] = utilisateur.user.last_name
                request.session['prenom'] = utilisateur.user.first_name
                request.session['telephone'] = utilisateur.telephone
                request.session['date_nais'] = utilisateur.date_nais.strftime('%Y-%m-%d')
                request.session['civilite'] = utilisateur.civilite
                request.session['role'] = utilisateur.role
                request.session['email'] = utilisateur.user.email
                request.session['genre'] = utilisateur.genre
                t = request.session['mot_de_passe'] = utilisateur.user.password
                print(t)
                request.session['imagesprofiles'] = utilisateur.imagesprofiles.url
                request.session['cycle'] = utilisateur.cycle
                request.session['filiere'] = utilisateur.filiere
                request.session['niveaux'] = utilisateur.niveaux
                return redirect('student_space')
            elif isinstance(utilisateur, CSS):
                # Redirigez l'utilisateur en fonction de son rôle
                return redirect('cssWork')
        else:
            error_message = "Email et/ou Mot de passe Incorrect ! réessayez."

    return render(request, 'login.html', {'error_message': error_message})
