from django.shortcuts import redirect
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from axes.models import AccessAttempt


def custom_lockout_response(request, credentials, *args, **kwargs):
    ip_address = request.axes_ip_address
    account = AccessAttempt.objects.filter(ip_address=ip_address).first()
    COOLOFF_TIME = timezone.timedelta(hours=settings.AXES_COOLOFF_TIME)
    time_elapsed = timezone.now() - account.attempt_time
    wait_time = COOLOFF_TIME - time_elapsed

    # Format wait_time
    wait_hours, remainder = divmod(wait_time.seconds, 3600)
    wait_minutes, wait_seconds = divmod(remainder, 60)

    wait_time_formatted = f"{wait_hours}:{wait_minutes}:{wait_seconds}"

    messages.error(request, _('You are locked for too many requests. Please wait for %(wait_time)s' % {
        'wait_time': wait_time_formatted}))
    return redirect('account_login')
