from django.shortcuts import render

# Create your views here.
def cssWork(request):
    nom = request.session.get('nom')
    imagesprofiles = request.session.get('imagesprofiles')
    return render(request, 'pages/index-css.html',  {'nom': nom , 'imagesprofiles': imagesprofiles})