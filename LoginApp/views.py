from django.shortcuts import render, redirect
from EtudiantApp.data_models.etudiant import Etudiant
from CSSAPP.data_models.css import CSS
from DCFISPACE.data_models.directeur import Directeur
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from Utilisateur.data_models.utilisateur import Utilisateur
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist


# def sign_in(request):
#     error_message = None

#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('your_pass')
#         remember_me_cookies = request.POST.get('remember-me')

#         try:
#             # Essayez de récupérer un étudiant ou un CSS avec l'email donné
#             utilisateur = Etudiant.objects.get(user__email=email)
#         except Etudiant.DoesNotExist:
#             try:
#                 utilisateur = CSS.objects.get(user__email=email)
                
#             except CSS.DoesNotExist:
#                 try:
#                     # Essayez de récupérer un Directeur avec l'email donné
#                     utilisateur = Directeur.objects.get(user__email=email)
#                 except Directeur.DoesNotExist:
#                     # Utilisateur non trouvé
#                     error_message = "Email et/ou Mot de passe Incorrect ! réessayez."
#                     messages.error(request, error_message)
#                     return render(request, 'login.html', {'error_message': error_message})
                
#         # Vérifiez le mot de passe en utilisant la méthode check_password
#         if utilisateur.user.check_password(password):
#             if remember_me_cookies:
#                 response = HttpResponse() 
#                 remember_me(request, response, utilisateur.user)
#                 response.set_cookie('matricule', utilisateur)
#                 return response  
              
                
#             if utilisateur.first_login:
#                 request.session['user_to_change_password'] = utilisateur.user.id
#                 request.session['email'] = utilisateur.user.email
#                 # print(t)
#                 # Rediriger vers la réinitialisation du mot de passe lors de la première connexion
#                 return redirect('change_password')  
#             else:
#             # Authentification réussie, connectez l'utilisateur
#                 login(request, utilisateur.user)

#                 if isinstance(utilisateur, Etudiant):
#                     # Redirigez l'utilisateur en fonction de son rôle
#                     request.session['matricule'] = utilisateur.matricule
#                     request.session['Identification'] = utilisateur.Identification
#                     request.session['nom'] = utilisateur.user.last_name
#                     request.session['prenom'] = utilisateur.user.first_name
#                     request.session['telephone'] = utilisateur.telephone
#                     request.session['date_nais'] = utilisateur.date_nais.strftime('%Y-%m-%d')
#                     request.session['civilite'] = utilisateur.civilite
#                     request.session['role'] = utilisateur.role
#                     request.session['email'] = utilisateur.user.email
#                     request.session['genre'] = utilisateur.genre
#                     t = request.session['mot_de_passe'] = utilisateur.user.password
#                     print(t)
#                     request.session['imagesprofiles'] = utilisateur.imagesprofiles.url
#                     request.session['cycle'] = utilisateur.cycle
#                     request.session['filiere'] = utilisateur.filiere
#                     request.session['niveaux'] = utilisateur.niveaux
#                     return redirect('student_space')
#                 elif isinstance(utilisateur, CSS):
#                     # Redirigez l'utilisateur en fonction de son rôle
#                     request.session['matricule'] = utilisateur.matricule
#                     request.session['nom'] = utilisateur.user.last_name
#                     request.session['prenom'] = utilisateur.user.first_name
#                     request.session['telephone'] = utilisateur.telephone
#                     request.session['date_nais'] = utilisateur.date_nais.strftime('%Y-%m-%d')
#                     request.session['civilite'] = utilisateur.civilite
#                     request.session['role'] = utilisateur.role
#                     request.session['email'] = utilisateur.user.email
#                     request.session['genre'] = utilisateur.genre
#                     t = request.session['mot_de_passe'] = utilisateur.user.password
#                     print(t)
#                     request.session['imagesprofiles'] = utilisateur.imagesprofiles.url
#                     return redirect('cssWork')
                
#                 elif isinstance(utilisateur, Directeur):
#                     # Redirigez l'utilisateur en fonction de son rôle
#                     request.session['matricule'] = utilisateur.matricule
#                     request.session['nom'] = utilisateur.user.last_name
#                     request.session['prenom'] = utilisateur.user.first_name
#                     request.session['telephone'] = utilisateur.telephone
#                     request.session['date_nais'] = utilisateur.date_nais.strftime('%Y-%m-%d')
#                     request.session['civilite'] = utilisateur.civilite
#                     request.session['role'] = utilisateur.role
#                     request.session['email'] = utilisateur.user.email
#                     request.session['genre'] = utilisateur.genre
#                     t = request.session['mot_de_passe'] = utilisateur.user.password
#                     print(t)
#                     request.session['imagesprofiles'] = utilisateur.imagesprofiles.url
#                     return redirect('Home_Directeur')
#         else:
#             error_message = "Email et/ou Mot de passe Incorrect ! réessayez."

#     return render(request, 'login.html', {'error_message': error_message})




def sign_in(request):
    error_message = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('your_pass')
        remember_me_cookies = request.POST.get('remember-me')

        try:
            # Essayez de récupérer un étudiant ou un CSS avec l'email donné
            utilisateur = Etudiant.objects.get(user__email=email)
        except Etudiant.DoesNotExist:
            try:
                utilisateur = CSS.objects.get(user__email=email)
            except CSS.DoesNotExist:
                try:
                    # Essayez de récupérer un Directeur avec l'email donné
                    utilisateur = Directeur.objects.get(user__email=email)
                except Directeur.DoesNotExist:
                    # Utilisateur non trouvé
                    error_message = "Email et/ou Mot de passe Incorrect ! réessayez."
                    messages.error(request, error_message)
                    return render(request, 'login.html', {'error_message': error_message})

        # Vérifiez le mot de passe en utilisant la méthode check_password
        if utilisateur.user.check_password(password):
            if remember_me_cookies:
                response = HttpResponse()
                response.set_cookie('email', utilisateur.user.email, max_age=30 * 24 * 60 * 60)  # Définir le cookie "Remember me" pendant 30 jours
                response.set_cookie('password', utilisateur.user.password, max_age=30 * 24 * 60 * 60)
                # return response

            if utilisateur.first_login:
                request.session['user_to_change_password'] = utilisateur.user.id
                request.session['email'] = utilisateur.user.email
                # Rediriger vers la réinitialisation du mot de passe lors de la première connexion
                return redirect('change_password')
            else:
                # Authentification réussie, connectez l'utilisateur
                login(request, utilisateur.user)

                if isinstance(utilisateur, Etudiant):
                    # Rediriger l'utilisateur en fonction de son rôle
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
                    request.session['mot_de_passe'] = utilisateur.user.password
                    request.session['imagesprofiles'] = utilisateur.imagesprofiles.url
                    request.session['cycle'] = utilisateur.cycle
                    request.session['filiere'] = utilisateur.filiere
                    request.session['niveaux'] = utilisateur.niveaux
                    return redirect('student_space')
                elif isinstance(utilisateur, CSS):
                    # Rediriger l'utilisateur en fonction de son rôle
                    request.session['matricule'] = utilisateur.matricule
                    request.session['nom'] = utilisateur.user.last_name
                    request.session['prenom'] = utilisateur.user.first_name
                    request.session['telephone'] = utilisateur.telephone
                    request.session['date_nais'] = utilisateur.date_nais.strftime('%Y-%m-%d')
                    request.session['civilite'] = utilisateur.civilite
                    request.session['role'] = utilisateur.role
                    request.session['email'] = utilisateur.user.email
                    request.session['genre'] = utilisateur.genre
                    request.session['mot_de_passe'] = utilisateur.user.password
                    request.session['imagesprofiles'] = utilisateur.imagesprofiles.url
                    return redirect('cssWork')

                elif isinstance(utilisateur, Directeur):
                    # Rediriger l'utilisateur en fonction de son rôle
                    request.session['matricule'] = utilisateur.matricule
                    request.session['nom'] = utilisateur.user.last_name
                    request.session['prenom'] = utilisateur.user.first_name
                    request.session['telephone'] = utilisateur.telephone
                    request.session['date_nais'] = utilisateur.date_nais.strftime('%Y-%m-%d')
                    request.session['civilite'] = utilisateur.civilite
                    request.session['role'] = utilisateur.role
                    request.session['email'] = utilisateur.user.email
                    request.session['genre'] = utilisateur.genre
                    request.session['mot_de_passe'] = utilisateur.user.password
                    request.session['imagesprofiles'] = utilisateur.imagesprofiles.url
                    return redirect('Home_Directeur')
        else:
            error_message = "Email et/ou Mot de passe Incorrect ! réessayez."

    return render(request, 'login.html', {'error_message': error_message})


# def remember_me(request, response, user):
#     if request.POST.get('remember-me'):
#         # Définir un cookie de "Remember Me" avec une durée de validité plus longue
#         response.set_cookie('remember_me', user.id, max_age=604800)  # Exemple : 1 semaine (en secondes)
#         # Enregistrer également le type de profil dans le cookie pour la récupération dans auto_login
#         response.set_cookie('user_profile', user.__class__.__name__, max_age=604800)
#         return response


# def auto_login(request):
#     if 'remember_me' in request.COOKIES:
#         user_id = request.COOKIES['remember_me']
#         user_profile = request.COOKIES['user_profile']
        
#         try:
#             # Utiliser le type de profil récupéré pour obtenir le bon modèle utilisateur
#             if user_profile == 'Etudiant':
#                 user = Etudiant.objects.get(id=user_id).user
#                 return redirect('student_space')  # Redirection vers l'espace étudiant
#             elif user_profile == 'CSS':
#                 user = CSS.objects.get(id=user_id).user
#                 return redirect('cssWork')  # Redirection vers l'espace CSS
#             elif user_profile == 'Directeur':
#                 user = Directeur.objects.get(id=user_id).user
#                 return redirect('Home_Directeur')  # Redirection vers l'espace Directeur
            
#             login(request, user)
#         except ObjectDoesNotExist:
#             # Gérer le cas où l'utilisateur n'est pas trouvé dans la base de données
#             # Vous pouvez afficher un message d'erreur ou effectuer d'autres actions nécessaires
#             print("L'utilisateur n'a pas été trouvé dans la base de données.")

#     # Rediriger vers la page de connexion si la connexion automatique n'est pas réussie
#     return redirect('SignInView')


# def change_password(request):
#     if request.method == 'POST':
#         new_password1 = request.POST.get('password')
#         new_password2 = request.POST.get('confirmPassword')

#         if new_password1 and new_password2:
#             # Récupérez l'adresse e-mail de l'utilisateur depuis la session
#             email = request.session.get('email')
#             user_id = request.session.get('user_to_change_password')
#             print(email)
#             print(user_id)

#             if email and user_id:
#                 try:
#                     # Vérifiez si l'utilisateur est un étudiant
#                     etudiant = Etudiant.objects.get(user__email=email)

#                     # Vérifiez si l'utilisateur est un étudiant et que c'est sa première connexion
#                     if etudiant and etudiant.first_login:
#                         # Récupérez l'utilisateur à partir de l'ID
#                         user = User.objects.get(id=user_id)

#                         # Si c'est sa première connexion, changez le mot de passe
#                         if new_password1 == new_password2:
#                             user.set_password(new_password1)
#                             etudiant.first_login = False
#                             user.save()
#                             etudiant.save()
#                             update_session_auth_hash(request, user)
#                             messages.success(request, 'Votre mot de passe a été changé avec succès!')
#                             return redirect('SignInView')
#                         else:
#                             messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
#                     elif etudiant:
#                         # Si c'est un étudiant mais ce n'est pas sa première connexion, redirigez vers SignInView
#                         return redirect('SignInView')

#                 except Etudiant.DoesNotExist:
#                     pass
                
#                 try:
#                     # Vérifiez si l'utilisateur est de type CSS
#                     css = CSS.objects.get(user__email=email)

#                     # Vérifiez si l'utilisateur est un CSS et que c'est sa première connexion
#                     if css and css.first_login:
#                         # Récupérez l'utilisateur à partir de l'ID
#                         user = User.objects.get(id=user_id)

#                         # Si c'est sa première connexion, changez le mot de passe
#                         if new_password1 == new_password2:
#                             user.set_password(new_password1)
#                             css.first_login = False
#                             user.save()
#                             css.save()
#                             update_session_auth_hash(request, user)
#                             messages.success(request, 'Votre mot de passe a été changé avec succès!')
#                             return redirect('SignInView')
#                         else:
#                             messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
#                     elif css:
#                         # Si c'est un CSS mais ce n'est pas sa première connexion, redirigez vers SignInView
#                         return redirect('SignInView')

#                 except CSS.DoesNotExist:
#                     pass

#                 # Si l'utilisateur n'est ni étudiant ni CSS, redirigez vers SignInView
#                 return redirect('SignInView')
                
#             else:
#                 messages.error(request, 'Adresse e-mail ou ID d\'utilisateur non trouvé dans la session.')
#         else:
#             messages.error(request, 'Veuillez remplir tous les champs.')

#     return render(request, 'password_reset.html')


# def change_password(request):
#     if request.method == 'POST':
#         new_password1 = request.POST.get('password')
#         new_password2 = request.POST.get('confirmPassword')
        
#         print(new_password2)

#         if new_password1 and new_password2:
#             # Récupérez l'adresse e-mail de l'utilisateur depuis la session
#             email = request.session.get('email')
#             user_id = request.session.get('user_to_change_password')
#             print(email)
#             print(user_id)

#             if email and user_id:
#                 try:
#                     # Vérifiez le type d'utilisateur (étudiant, CSS, directeur)
#                     etudiant = Etudiant.objects.get(user__email=email)
#                     utilisateur = etudiant

#                     if etudiant and etudiant.first_login:
#                         # Vérifiez la longueur minimale du mot de passe
#                         if len(new_password1) < 8:
#                             messages.error(request, 'Le mot de passe doit avoir au moins 8 caractères.')
#                             return render(request, 'password_reset.html', {'error_message': 'Le mot de passe doit avoir au moins 8 caractères.'})

#                         # Récupérez l'utilisateur à partir de l'ID
#                         user = User.objects.get(id=user_id)

#                         # Changez le mot de passe
#                         if new_password1 == new_password2:
#                             user.set_password(new_password1)
#                             utilisateur.first_login = False
#                             user.save()
#                             utilisateur.save()
#                             update_session_auth_hash(request, user)
#                             messages.success(request, 'Votre mot de passe a été changé avec succès!')
#                             return redirect('SignInView')
#                         else:
#                             messages.error(request, 'Les deux mots de passe ne correspondent pas. Veuillez corriger les erreurs ci-dessous.')
#                             return render(request, 'password_reset.html', {'error_message': 'Les deux mots de passe ne correspondent pas.'})
#                     elif etudiant:
#                         # Si c'est un étudiant mais ce n'est pas sa première connexion, redirigez vers SignInView
#                         return redirect('SignInView')

#                 except Etudiant.DoesNotExist:
#                     pass
                
#                 try:
#                     # Vérifiez si l'utilisateur est de type CSS
#                     css = CSS.objects.get(user__email=email)
#                     utilisateur = css

#                     if css and css.first_login:
#                         # Vérifiez la longueur minimale du mot de passe
#                         if len(new_password1) < 8:
#                             messages.error(request, 'Le mot de passe doit avoir au moins 8 caractères.')
#                             return render(request, 'password_reset.html', {'error_message': 'Le mot de passe doit avoir au moins 8 caractères.'})

#                         # Récupérez l'utilisateur à partir de l'ID
#                         user = User.objects.get(id=user_id)

#                         # Changez le mot de passe
#                         if new_password1 == new_password2:
#                             user.set_password(new_password1)
#                             utilisateur.first_login = False
#                             user.save()
#                             utilisateur.save()
#                             update_session_auth_hash(request, user)
#                             messages.success(request, 'Votre mot de passe a été changé avec succès!')
#                             return redirect('SignInView')
#                         else:
#                             messages.error(request, 'Les deux mots de passe ne correspondent pas. Veuillez corriger les erreurs ci-dessous.')
#                             return render(request, 'password_reset.html', {'error_message': 'Les deux mots de passe ne correspondent pas.'})
#                     elif css:
#                         # Si c'est un CSS mais ce n'est pas sa première connexion, redirigez vers SignInView
#                         return redirect('SignInView')

#                 except CSS.DoesNotExist:
#                     pass

#                 try:
#                     # Vérifiez si l'utilisateur est de type Directeur
#                     directeur = Directeur.objects.get(user__email=email)
#                     utilisateur = directeur

#                     if directeur and directeur.first_login:
#                         # Vérifiez la longueur minimale du mot de passe
#                         if len(new_password1) < 8:
#                             messages.error(request, 'Le mot de passe doit avoir au moins 8 caractères.')
#                             return render(request, 'password_reset.html', {'error_message': 'Le mot de passe doit avoir au moins 8 caractères.'})

#                         # Récupérez l'utilisateur à partir de l'ID
#                         user = User.objects.get(id=user_id)

#                         # Changez le mot de passe
#                         if new_password1 == new_password2:
#                             user.set_password(new_password1)
#                             utilisateur.first_login = False
#                             user.save()
#                             utilisateur.save()
#                             update_session_auth_hash(request, user)
#                             messages.success(request, 'Votre mot de passe a été changé avec succès!')
#                             return redirect('SignInView')
#                         else:
#                             messages.error(request, 'Les deux mots de passe ne correspondent pas. Veuillez corriger les erreurs ci-dessous.')
#                             return render(request, 'password_reset.html', {'error_message': 'Les deux mots de passe ne correspondent pas.'})
#                     elif directeur:
#                         # Si c'est un Directeur mais ce n'est pas sa première connexion, redirigez vers SignInView
#                         return redirect('SignInView')

#                 except Directeur.DoesNotExist:
#                     pass

#                 # Si l'utilisateur n'est ni étudiant, ni CSS, ni Directeur, redirigez vers SignInView
#                 return redirect('SignInView')
                
#             else:
#                 messages.error(request, 'Adresse e-mail ou ID d\'utilisateur non trouvé dans la session.')
#         else:
#             messages.error(request, 'Veuillez remplir tous les champs.')

#     return render(request, 'password_reset.html')



def change_password(request):
    if request.method == 'POST':
        new_password1 = request.POST.get('password')
        new_password2 = request.POST.get('confirmPassword')
        
        if new_password1 and new_password2:
            email = request.session.get('email')
            user_id = request.session.get('user_to_change_password')
            
            if email and user_id:
                try:
                    etudiant = Etudiant.objects.get(user__email=email)

                    if etudiant and etudiant.first_login:
                        if len(new_password1) < 8:
                            messages.error(request, 'Le mot de passe doit avoir au moins 8 caractères.')
                            return render(request, 'password_reset.html', {'error_message': 'Le mot de passe doit avoir au moins 8 caractères.'})

                        user = User.objects.get(id=user_id)
                        if new_password1 == new_password2:
                            user.set_password(new_password1)
                            etudiant.first_login = False
                            user.save()
                            etudiant.save()
                            update_session_auth_hash(request, user)
                            messages.success(request, 'Votre mot de passe a été changé avec succès!')
                            return redirect('SignInView')
                        else:
                            messages.error(request, 'Les deux mots de passe ne correspondent pas. Veuillez corriger les erreurs ci-dessous.')
                            return render(request, 'password_reset.html', {'error_message': 'Les deux mots de passe ne correspondent pas.'})
                    elif etudiant:
                        return redirect('SignInView')

                except Etudiant.DoesNotExist:
                    pass
                
                try:
                    css = CSS.objects.get(user__email=email)

                    if css and css.first_login:
                        if len(new_password1) < 8:
                            messages.error(request, 'Le mot de passe doit avoir au moins 8 caractères.')
                            return render(request, 'password_reset.html', {'error_message': 'Le mot de passe doit avoir au moins 8 caractères.'})

                        user = User.objects.get(id=user_id)
                        if new_password1 == new_password2:
                            user.set_password(new_password1)
                            css.first_login = False
                            user.save()
                            css.save()
                            update_session_auth_hash(request, user)
                            messages.success(request, 'Votre mot de passe a été changé avec succès!')
                            return redirect('SignInView')
                        else:
                            messages.error(request, 'Les deux mots de passe ne correspondent pas. Veuillez corriger les erreurs ci-dessous.')
                            return render(request, 'password_reset.html', {'error_message': 'Les deux mots de passe ne correspondent pas.'})
                    elif css:
                        return redirect('SignInView')

                except CSS.DoesNotExist:
                    pass

                try:
                    directeur = Directeur.objects.get(user__email=email)

                    if directeur and directeur.first_login:
                        if len(new_password1) < 8:
                            messages.error(request, 'Le mot de passe doit avoir au moins 8 caractères.')
                            return render(request, 'password_reset.html', {'error_message': 'Le mot de passe doit avoir au moins 8 caractères.'})

                        user = User.objects.get(id=user_id)
                        if new_password1 == new_password2:
                            user.set_password(new_password1)
                            directeur.first_login = False
                            user.save()
                            directeur.save()
                            update_session_auth_hash(request, user)
                            messages.success(request, 'Votre mot de passe a été changé avec succès!')
                            return redirect('SignInView')
                        else:
                            messages.error(request, 'Les deux mots de passe ne correspondent pas. Veuillez corriger les erreurs ci-dessous.')
                            return render(request, 'password_reset.html', {'error_message': 'Les deux mots de passe ne correspondent pas.'})
                    elif directeur:
                        return redirect('SignInView')

                except Directeur.DoesNotExist:
                    pass

                return redirect('SignInView')
                
            else:
                messages.error(request, 'Adresse e-mail ou ID d\'utilisateur non trouvé dans la session.')
        else:
            messages.error(request, 'Veuillez remplir tous les champs.')

    return render(request, 'password_reset.html')