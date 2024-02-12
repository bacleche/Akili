from EtudiantApp.data_models.notifications import Notification
from django.utils import timezone


class DeleteExpiredNotificationsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Supprimer les notifications expirées avant de traiter la requête
        Notification.objects.filter(date_creation__lte=timezone.now() - timezone.timedelta(days=7)).delete()
        response = self.get_response(request)
        return response