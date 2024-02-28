from django.utils import timezone

from apps.authentication_app.models import CustomUser

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class UpdateUserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            CustomUser.objects.filter(pk=request.user.id).update(last_activity=timezone.now(), is_online=True)

            # отправка айдишника пользователя, который в данный момент активен
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'update_status_group', {
                    'type': 'set_online_status_user',
                    'active_user_id': request.user.id
                }
            )

        return response