from django.shortcuts import render
from django.views.generic import View

from fcm_django.models import FCMDevice

from core.models import NotificationHistory
# Create your views here.

class IndexView(View):
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class NotificationView(View):
    template_name = 'core/notification_form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        fcm_token = request.POST.get('fcmToken')
        notification_text = request.POST.get('notification_text')
        notification_icon = request.POST.get('notification_icon')

        nf = NotificationHistory.objects.create(
            fcm_token=fcm_token,
            notification_text=notification_text,
            notification_icon=notification_icon,
            )
        notification_icon_url = request.build_absolute_uri(nf.notification_icon.url)

        devices = FCMDevice.objects.filter(
            registration_id=fcm_token
            )

        devices.send_message(
            title="Demo Notification Created by Gaurav", 
            body=notification_text, 
            icon=notification_icon_url, 
            # data={"test": "test"}
        )

        return render(request, self.template_name)