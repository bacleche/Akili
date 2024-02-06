from django.shortcuts import render, redirect
from EtudiantApp.data_models.etudiant import Etudiant
from CSSAPP.data_models.css import CSS
from DCFISPACE.data_models.directeur import Directeur

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from Utilisateur.data_models.utilisateur import Utilisateur
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


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
            if utilisateur.first_login:
                request.session['user_to_change_password'] = utilisateur.user.id
                request.session['email'] = utilisateur.user.email
                # print(t)
                # Rediriger vers la réinitialisation du mot de passe lors de la première connexion
                return redirect('change_password')  
            else:
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
                    request.session['matricule'] = utilisateur.matricule
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
                    return redirect('cssWork')
                
                elif isinstance(utilisateur, Directeur):
                    # Redirigez l'utilisateur en fonction de son rôle
                    request.session['matricule'] = utilisateur.matricule
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
                    return redirect('Home_Directeur')
        else:
            error_message = "Email et/ou Mot de passe Incorrect ! réessayez."

    return render(request, 'login.html', {'error_message': error_message})


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


def change_password(request):
    if request.method == 'POST':
        new_password1 = request.POST.get('password')
        new_password2 = request.POST.get('confirmPassword')

        if new_password1 and new_password2:
            # Récupérez l'adresse e-mail de l'utilisateur depuis la session
            email = request.session.get('email')
            user_id = request.session.get('user_to_change_password')

            if email and user_id:
                try:
                    # Vérifiez le type d'utilisateur (étudiant, CSS, directeur)
                    etudiant = Etudiant.objects.get(user__email=email)
                    utilisateur = etudiant

                    if etudiant and etudiant.first_login:
                        # Vérifiez la longueur minimale du mot de passe
                        if len(new_password1) < 8:
                            messages.error(request, 'Le mot de passe doit avoir au moins 8 caractères.')
                            return render(request, 'password_reset.html', {'error_message': 'Le mot de passe doit avoir au moins 8 caractères.'})

                        # Récupérez l'utilisateur à partir de l'ID
                        user = User.objects.get(id=user_id)

                        # Changez le mot de passe
                        if new_password1 == new_password2:
                            user.set_password(new_password1)
                            utilisateur.first_login = False
                            user.save()
                            utilisateur.save()
                            update_session_auth_hash(request, user)
                            messages.success(request, 'Votre mot de passe a été changé avec succès!')
                            return redirect('SignInView')
                        else:
                            messages.error(request, 'Les deux mots de passe ne correspondent pas. Veuillez corriger les erreurs ci-dessous.')
                            return render(request, 'password_reset.html', {'error_message': 'Les deux mots de passe ne correspondent pas.'})
                    elif etudiant:
                        # Si c'est un étudiant mais ce n'est pas sa première connexion, redirigez vers SignInView
                        return redirect('SignInView')

                except Etudiant.DoesNotExist:
                    pass
                
                try:
                    # Vérifiez si l'utilisateur est de type CSS
                    css = CSS.objects.get(user__email=email)
                    utilisateur = css

                    if css and css.first_login:
                        # Vérifiez la longueur minimale du mot de passe
                        if len(new_password1) < 8:
                            messages.error(request, 'Le mot de passe doit avoir au moins 8 caractères.')
                            return render(request, 'password_reset.html', {'error_message': 'Le mot de passe doit avoir au moins 8 caractères.'})

                        # Récupérez l'utilisateur à partir de l'ID
                        user = User.objects.get(id=user_id)

                        # Changez le mot de passe
                        if new_password1 == new_password2:
                            user.set_password(new_password1)
                            utilisateur.first_login = False
                            user.save()
                            utilisateur.save()
                            update_session_auth_hash(request, user)
                            messages.success(request, 'Votre mot de passe a été changé avec succès!')
                            return redirect('SignInView')
                        else:
                            messages.error(request, 'Les deux mots de passe ne correspondent pas. Veuillez corriger les erreurs ci-dessous.')
                            return render(request, 'password_reset.html', {'error_message': 'Les deux mots de passe ne correspondent pas.'})
                    elif css:
                        # Si c'est un CSS mais ce n'est pas sa première connexion, redirigez vers SignInView
                        return redirect('SignInView')

                except CSS.DoesNotExist:
                    pass

                try:
                    # Vérifiez si l'utilisateur est de type Directeur
                    directeur = Directeur.objects.get(user__email=email)
                    utilisateur = directeur

                    if directeur and directeur.first_login:
                        # Vérifiez la longueur minimale du mot de passe
                        if len(new_password1) < 8:
                            messages.error(request, 'Le mot de passe doit avoir au moins 8 caractères.')
                            return render(request, 'password_reset.html', {'error_message': 'Le mot de passe doit avoir au moins 8 caractères.'})

                        # Récupérez l'utilisateur à partir de l'ID
                        user = User.objects.get(id=user_id)

                        # Changez le mot de passe
                        if new_password1 == new_password2:
                            user.set_password(new_password1)
                            utilisateur.first_login = False
                            user.save()
                            utilisateur.save()
                            update_session_auth_hash(request, user)
                            messages.success(request, 'Votre mot de passe a été changé avec succès!')
                            return redirect('SignInView')
                        else:
                            messages.error(request, 'Les deux mots de passe ne correspondent pas. Veuillez corriger les erreurs ci-dessous.')
                            return render(request, 'password_reset.html', {'error_message': 'Les deux mots de passe ne correspondent pas.'})
                    elif directeur:
                        # Si c'est un Directeur mais ce n'est pas sa première connexion, redirigez vers SignInView
                        return redirect('SignInView')

                except Directeur.DoesNotExist:
                    pass

                # Si l'utilisateur n'est ni étudiant, ni CSS, ni Directeur, redirigez vers SignInView
                return redirect('SignInView')
                
            else:
                messages.error(request, 'Adresse e-mail ou ID d\'utilisateur non trouvé dans la session.')
        else:
            messages.error(request, 'Veuillez remplir tous les champs.')

    return render(request, 'password_reset.html')