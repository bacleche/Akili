from django.shortcuts import render, redirect
from EtudiantApp.data_models.etudiant import Etudiant
from CSSAPP.data_models.css import CSS
from django.contrib import messages


def sign_in(request):
    error_message = None  
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('your_pass')
        etudiant = Etudiant.objects.filter(email=email).first()
        print(etudiant)
        css = CSS.objects.filter(email=email).first()
        print(css)
        if etudiant and etudiant.mot_de_passe == password:
                request.session['matricule'] = etudiant.matricule
                request.session['nom'] = etudiant.nom
                request.session['prenom'] = etudiant.prenom
                request.session['civilite'] = etudiant.civilite
                request.session['email'] = etudiant.email
                request.session['role'] = etudiant.role
                request.session['genre'] = etudiant.genre
                request.session['telephone'] = etudiant.telephone
                request.session['date_nais'] = etudiant.date_nais.strftime('%Y-%m-%d')
                request.session['mot_de_passe'] = etudiant.mot_de_passe
                request.session['confirmer_mot_de_passe'] = etudiant.confirmer_mot_de_passe
                request.session['imagesprofiles'] = etudiant.imagesprofiles.url 
                return redirect('student_space')
        
       
        elif css and css.mot_de_passe == password:
                request.session['matricule'] = css.matricule
                request.session['nom'] = css.nom
                request.session['prenom'] = css.prenom
                request.session['civilite'] = css.civilite
                request.session['email'] = css.email
                request.session['role'] = css.role 
                request.session['genre'] = css.genre 
                request.session['telephone'] = css.telephone 
                request.session['date_nais'] = css.date_nais.strftime('%Y-%m-%d')
                request.session['mot_de_passe'] = css.mot_de_passe
                request.session['confirmer_mot_de_passe'] = css.confirmer_mot_de_passe
                request.session['imagesprofiles'] = css.imagesprofiles.url 
                return redirect('cssWork')
        else : 
            print('rate')
        error_message = "L'authentification a échoué. Veuillez vérifier vos identifiants."

    return render(request, 'login.html', {'error_message': error_message})
