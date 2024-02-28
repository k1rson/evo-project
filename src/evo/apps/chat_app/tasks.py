from evo.celery import app

from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from apps.authentication_app.models import CustomUser

@app.task
def check_user_activity():
    inactive_users = CustomUser.objects.filter(last_activity__lte=timezone.now() - timezone.timedelta(minutes=5), is_online=True)
    if inactive_users:
        inactive_users_ids = list(inactive_users.values_list('id', flat=True))

        CustomUser.objects.filter(id__in=inactive_users_ids).update(is_online=False)

        # отправка пачки айдишников с неактивными пользователями в канальный слой обновления статуса
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'update_status_group', {
                'type': 'set_offline_status_user',
                'inactive_users_ids': inactive_users_ids
            }
        )