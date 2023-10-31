from django.urls import path
from . import views

urlpatterns = [
    path('css_space', views.cssWork, name='cssWork'),
]