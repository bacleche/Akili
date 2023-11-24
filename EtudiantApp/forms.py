from django import forms
from EtudiantApp.data_models.memoire import Memoire
from EtudiantApp.data_models.etudiant import Etudiant
from django.db import models


class MemoireForm(forms.ModelForm):
    class Meta:
        model = Memoire
        fields = ['titre', 'date_poste', 'identite', 'co_auteur' , 'document']

    def __init__(self, *args, **kwargs):
        # Récupérez l'utilisateur connecté depuis les kwargs
        user_data = kwargs.pop('user_data', None)
        super().__init__(*args, **kwargs)

        # Filtrez les choix du champ identite pour inclure uniquement l'étudiant connecté
        if user_data:
            self.fields['co_auteur'].queryset = Etudiant.objects.exclude(matricule=user_data['matricule'])
            
            
        if user_data:
            self.fields['identite'].queryset = Etudiant.objects.filter(matricule=user_data['matricule'])


        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        identite = cleaned_data.get('identite')
        co_auteur = cleaned_data.get('co_auteur')

        if co_auteur:
            if (
                getattr(co_auteur, 'niveaux', None) != getattr(identite, 'niveaux', None)
                or getattr(co_auteur, 'cycle', None) != getattr(identite, 'cycle', None)
                or getattr(co_auteur, 'filiere', None) != getattr(identite, 'filiere', None)
            ):
                raise forms.ValidationError("Le co-auteur doit être du même niveau et de la même option.")
        existing_memoires = Memoire.objects.filter(
            models.Q(identite=identite) | models.Q(co_auteur=identite) |
            models.Q(identite=co_auteur) | models.Q(co_auteur=co_auteur)
        )

        existing_memoires = Memoire.objects.filter(identite=identite, co_auteur=co_auteur)
        if self.instance.pk:
            existing_memoires = existing_memoires.exclude(pk=self.instance.pk)

        if existing_memoires.exists():
                raise forms.ValidationError("Vous ne pouvez publier qu'un seul mémoire avec ces identités.")
