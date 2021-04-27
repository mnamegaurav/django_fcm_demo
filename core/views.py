from django.shortcuts import render
from django.views.generic import View

from fcm_django.models import FCMDevice

from core.models import NotificationHistory

from core.forms import NotificationHistoryForm
# Create your views here.

class IndexView(View):
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class NotificationView(View):
    template_name = 'core/notification_form.html'
    form_class = NotificationHistoryForm

    def get(self, request, *args, **kwargs):
        context = {'form': self.form_class()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            context = {'form': self.form_class()}
        else:
            context = {'form': form}

        fcm_token = form.cleaned_data.get('fcm_token')
        notification_text = form.cleaned_data.get('notification_text')
        notification_title = form.cleaned_data.get('notification_title')
        notification_icon = form.cleaned_data.get('notification_icon')
        notification_image = form.cleaned_data.get('notification_image')


        if notification_icon:
            notification_icon_url = request.build_absolute_uri(notification_icon.url)
        else:
            notification_icon_url = ''

        if notification_image:
            notification_image_url = request.build_absolute_uri(notification_image.url)
        else:
            notification_image_url = ''

        devices = FCMDevice.objects.filter(
            registration_id=fcm_token
            )

        devices.send_message(
            title=notification_title, 
            body=notification_text, 
            icon=notification_icon_url, 
            data={
                "image": notification_image_url,
            }
        )

        return render(request, self.template_name, context)