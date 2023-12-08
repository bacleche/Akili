from EtudiantApp.data_models.etudiant import Etudiant
from EtudiantApp.data_models.notifications import Notification
from django.core.exceptions import ObjectDoesNotExist

def notifications_non_lues(request):
    user_data = {key: request.session.get(key) for key in ['matricule', 'Identification' , 'nom', 'prenom', 'telephone', 'date_nais', 'civilite', 'role', 'email', 'genre', 'mot_de_passe','confirmer_mot_de_passe', 'imagesprofiles']}

    binome = None
    notifications = None

    try:
        etudiant_connecte = Etudiant.objects.get(Identification=user_data['Identification'])
        binome = etudiant_connecte.Identification
        notifications = Notification.objects.filter(destinataire=etudiant_connecte, est_lue=False)
    except ObjectDoesNotExist:
        etudiant_connecte = None

    return {
        'notifications_non_lues': notifications,
        'binome': binome,
    }
