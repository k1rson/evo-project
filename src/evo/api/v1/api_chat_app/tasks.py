from celery import shared_task

from django.utils import timezone

from apps.authentication_app.models import CustomUser

@shared_task
def check_user_activity():
    print('CHECK USER ACTIVITY')
    inactive_threshold = timezone.now() - timezone.timedelta(minutes=5)
    inactive_users = CustomUser.objects.filter(last_activity__lt=inactive_threshold)
    inactive_users.update(is_online=False)
