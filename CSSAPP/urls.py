from django.urls import path
from . import views

urlpatterns = [
    path('css_space', views.cssWork, name='cssWork'),
    path('Profiles_css' , views.Profiles_css , name='Profiles_css'),
    path('update_profile' , views.profile_details , name='update_profile'),
    path('mis_a_jour' , views.mis_a_jour , name='mis_a_jour'),


]