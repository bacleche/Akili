from EtudiantApp.data_models.etudiant import Etudiant
from EtudiantApp.data_models.notifications import Notification
from django.core.exceptions import ObjectDoesNotExist
from DCFISPACE.data_models.directeur import Directeur
from CSSAPP.data_models.css import CSS



def notifications_non_lues(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification' , 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    binome = None
    notifications = None
    notifications2 = None

    try:
        etudiant_connecte = Etudiant.objects.get(Identification=user_data['Identification'])
        binome = etudiant_connecte.Identification
        notifications = Notification.objects.filter(destinataire=etudiant_connecte, est_lue=False)
        notifications2 = Notification.objects.filter(destinataire=etudiant_connecte, est_lue=True)
        
    except ObjectDoesNotExist:
        etudiant_connecte = None
        try:
            directeur_connecte = Directeur.objects.get(matricule=user_data['matricule'])
            notifications = Notification.objects.filter(destinataire_dir=directeur_connecte, est_lue=False)
            notifications2 = Notification.objects.filter(destinataire_dir=directeur_connecte, est_lue=True)
            print("********************direct**********")
        except ObjectDoesNotExist:
            directeur_connecte = None
            try:
                css_connecte = CSS.objects.get(matricule=user_data['matricule'])
                notifications = Notification.objects.filter(destinataire_css=css_connecte, est_lue=False)
                notifications2 = Notification.objects.filter(destinataire_css=css_connecte, est_lue=True)
                print("**********************css*****")
            except ObjectDoesNotExist:
                css_connecte = None

       
    return {
        'notifications_non_lues': notifications,
        'notifications_lues' : notifications2,
        'binome': binome,
    }







# def notifications_non_lues(request):
#     user_data = {key: request.session.get(key) for key in ['matricule', 'Identification' , 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}


#     dir_connecte = Directeur.objects.get(matricule=user_data['matricule'])
#     css_connecte = CSS.objects.get(matricule=user_data['matricule'])

#     css = css_connecte.matricule
#     notifications = Notification.objects.filter(destinataire_css=css_connecte, expediteur_dir=dir_connecte, est_lue=False)
#     notifications2 = Notification.objects.filter(destinataire_css=css_connecte, expediteur_dir=dir_connecte,  est_lue=True)
    


#     return {
#         'notifications_non_lues': notifications,
#         'notifications_lues' : notifications2,
#         'css': css,
#     }


# def notifications_non_lues(request):
#     user_data = {key: request.session.get(key) for key in ['matricule', 'Identification' , 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

#     notifications = None
#     notifications2 = None
#     profile_type = None

#     try:
#         if 'Identification' in user_data:
#             etudiant_connecte = Etudiant.objects.get(Identification=user_data['Identification'])
#             profile_type = 'Etudiant'
#             notifications = Notification.objects.filter(destinataire=etudiant_connecte)
#         elif 'matricule' in user_data:
#             dir_connecte = Directeur.objects.get(matricule=user_data['matricule'])
#             css_connecte = CSS.objects.get(matricule=user_data['matricule'])
#             profile_type = 'zz'
#             notifications = Notification.objects.filter(destinataire_css=css_connecte, expediteur_dir=dir_connecte)
        
#         if notifications:
#             notifications2 = notifications.filter(est_lue=True)
#             notifications = notifications.filter(est_lue=False)
        
#     except ObjectDoesNotExist:
#         pass

#     return {
#         'notifications_non_lues': notifications,
#         'notifications_lues': notifications2,
#         'profile_type': profile_type,
#     }


