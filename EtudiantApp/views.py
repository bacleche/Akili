from django.shortcuts import render

# Create your views here.
def EtudiantSPACE(request):
    return render(request, 'pages/index.html')