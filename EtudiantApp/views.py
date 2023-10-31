from django.shortcuts import render

# Create your views here.
def EtudiantSPACE(request):
    nom = request.session.get('nom') 
    imagesprofiles = request.session.get('imagesprofiles')
    return render(request, 'pages/index.html', {'nom': nom , 'imagesprofiles': imagesprofiles})