from django.urls import path
from . import views

urlpatterns = [
    path('css_space', views.cssWork, name='cssWork'),
    path('Profiles_css' , views.Profiles_css , name='Profiles_css'),
    path('update_profile' , views.profile_details , name='update_profile'),
    path('mis_a_jour_css' , views.mis_a_jour_css , name='mis_a_jour_css'), 
    path('list_demandes' , views.list_demandes , name='list_demandes'), 
    path('list_bulletin_demandes' , views.list_bulletin_demandes , name='list_bulletin_demandes'), 
    path('imprimer_demande_css/<int:demande_id>/', views.imprimer_demande_css, name='imprimer_demande_css'),
    path('deconnexion' , views.custom_logout , name='deconnexion'),

]    
