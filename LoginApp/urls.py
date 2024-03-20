from django.urls import path
from . import views

urlpatterns = [
    path('sign_in', views.sign_in, name='SignInView'),
    path('change_password' , views.change_password, name='change_password')

]