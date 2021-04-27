from django.db import models

# Create your models here.
class NotificationHistory(models.Model):
    fcm_token = models.TextField()
    notification_text = models.TextField()
    notification_icon = models.ImageField(upload_to='')

    def __str__(self):
        return self.fcm_token