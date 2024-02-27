from django.utils import timezone

from apps.authentication_app.models import CustomUser

class UpdateUserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            CustomUser.objects.filter(pk=request.user.id).update(last_activity=timezone.now())

        return response