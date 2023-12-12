from django import forms
from EtudiantApp.data_models.memoire import Memoire
from EtudiantApp.data_models.etudiant import Etudiant
from EtudiantApp.data_models.demande import Demande
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class MemoireForm(forms.ModelForm):
    class Meta:
        model = Memoire
        fields = ['titre', 'date_poste', 'identite', 'matricule_identification_binome', 'document']
        widgets = {
            'matricule_identification_binome': forms.TextInput(attrs={'required': False}),
        }

    def __init__(self, *args, **kwargs):
        # Récupérez l'utilisateur connecté depuis les kwargs
        user_data = kwargs.pop('user_data', None)
        super().__init__(*args, **kwargs)

        if user_data:
            self.fields['matricule_identification_binome'].queryset = Etudiant.objects.all()
            self.fields['identite'].queryset = Etudiant.objects.filter(matricule=user_data['matricule'])

        # Rendez le champ du binôme non obligatoire
        self.fields['matricule_identification_binome'].required = False

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



# class DemandeForm(forms.ModelForm):
#     class Meta:
#         model = Demande
#         fields = ['identite_concerne', 'objet_demande', 'session_dut', 'session_lic', 'filiere', 'cycle', 'annee_academique', 'identite_receptioniste']
#         widgets = {
#             'identite_concerne': forms.Select(attrs={'class': 'form-control'}),
#             'objet_demande': forms.Select(attrs={'class': 'form-control'}),
#             'session_dut': forms.Select(attrs={'class': 'form-control' , 'id': 'id_session_dut'}),
#             'session_lic': forms.Select(attrs={'class': 'form-control' , 'id': 'id_session_lic'}),
#             'filiere': forms.Select(attrs={'class': 'form-control'}),
#             'cycle': forms.Select(attrs={'class': 'form-control'}),
#             'annee_academique': forms.Select(attrs={'class': 'form-control'}),
#             'identite_receptioniste': forms.Select(attrs={'class': 'form-control'}),
#         }
        
#     def clean_annee_academique(self):
#         annee_academique = self.cleaned_data['annee_academique']
#         current_year = timezone.now().year

#         if int(annee_academique.split(' - ')[0]) > current_year:
#             raise forms.ValidationError("L'année académique ne peut pas être supérieure à l'année en cours.")

#         return annee_academique

#     def clean(self):
#         cleaned_data = super().clean()
#         cycle = cleaned_data.get('cycle')

#         if cycle == 'DUT':
#             session_lic = cleaned_data.get('session_lic')
#             if session_lic:
#                 raise forms.ValidationError("Le champ Session Licence doit être vide pour un cycle DUT.")
#         elif cycle == 'LICENCE':
#             session_dut = cleaned_data.get('session_dut')
#             if session_dut:
#                 raise forms.ValidationError("Le champ Session DUT doit être vide pour un cycle Licence.")
        
#         return cleaned_data


class DemandeForm(forms.ModelForm):
    class Meta:
        model = Demande
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user_data = kwargs.pop('user_data', None)
        super().__init__(*args, **kwargs)

        # Rendre les champs date_nais, genre et telephone non éditables
        self.fields['date_nais'].widget.attrs['readonly'] = True
        self.fields['genre'].widget.attrs['readonly'] = True
        self.fields['telephone'].widget.attrs['readonly'] = True
        self.fields['cycle'].widget.attrs['readonly'] = True
        self.fields['filiere'].widget.attrs['readonly'] = True
        self.fields['niveau'].widget.attrs['readonly'] = True




        # Pré-remplir les champs date_nais, genre et telephone si l'utilisateur est connecté
        if user_data:
            self.fields['date_nais'].initial = user_data.get('date_nais')
            self.fields['genre'].initial = user_data.get('genre')
            self.fields['telephone'].initial = user_data.get('telephone')
            self.fields['filiere'].initial = user_data.get('filiere')
            self.fields['cycle'].initial = user_data.get('cycle')
            self.fields['niveau'].initial = user_data.get('niveaux')


        # Ajouter les classes Bootstrap aux champs
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Masquer les champs session_dut et session_lic en fonction du type d'étudiant
        if user_data and user_data.get('cycle') == 'DUT':
            self.fields['session_lic'].widget = forms.HiddenInput()
            self.fields['session_lic'].widget.attrs['class'] = 'd-none'
        elif user_data and user_data.get('cycle') == 'Licence':
            self.fields['session_dut'].widget = forms.HiddenInput()
            self.fields['session_dut'].widget.attrs['class'] = 'd-none'