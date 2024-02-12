from EtudiantApp.data_models.etudiant import Etudiant
from EtudiantApp.data_models.notifications import Notification
from django.core.exceptions import ObjectDoesNotExist
from DCFISPACE.data_models.directeur import Directeur


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

    return {
        'notifications_non_lues': notifications,
        'notifications_lues' : notifications2,
        'binome': binome,
    }




def notifications_non_lues_dir(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification' , 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    dir = None
    notifications = None
    notifications2 = None

    try:
        dir_connecte = Directeur.objects.get(matricule=user_data['matricule'])
        dir = dir_connecte.matricule
        notifications = Notification.objects.filter(destinataire_dir=dir_connecte, est_lue=False)
        notifications2 = Notification.objects.filter(destinataire_dir=dir_connecte, est_lue=True)
        
    except ObjectDoesNotExist:
        etudiant_connecte = None

    return {
        'notifications_non_lues': notifications,
        'notifications_lues' : notifications2,
        'dir': dir,
    }
