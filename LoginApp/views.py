from django.shortcuts import render, redirect
from EtudiantApp.data_models.etudiant import Etudiant
from CSSAPP.data_models.css import CSS
from django.contrib import messages

def sign_in(request):
    error_message = None  # Initialisez la variable du message d'erreur à None
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
                request.session['imagesprofiles'] = etudiant.imagesprofiles.url 
                return redirect('student_space')
        
       
        elif css and css.mot_de_passe == password:
                request.session['matricule'] = css.matricule
                request.session['nom'] = css.nom
                request.session['imagesprofiles'] = css.imagesprofiles.url 
                return redirect('cssWork')
        else : 
            print('rate')
        error_message = "L'authentification a échoué. Veuillez vérifier vos identifiants."

    return render(request, 'login.html', {'error_message': error_message})
