from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.timezone import localtime

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "sent_messages")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "received_messages")
    text = models.CharField(max_length = 65535)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)
    is_public = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        if self.sender.is_politician:
            raise ValidationError("Politicians can't send messages")
        if not self.recipient.is_politician:
            raise ValidationError("Messages must go to politicians")
        super(Message, self).save(*args, **kwargs)
    
    def viewable_by_user(self, user):
        if user is None:
            return self.is_public
        return user == self.sender or user == self.recipient or (user.is_filterer and user.is_connected_to_politician(self.recipient))

    @property
    def tag(self):
        from yourvoice.apps.filterers.models import MessageTag
        try:
            return MessageTag.objects.get(message = self)
        except MessageTag.DoesNotExist:
            return None
    @property
    def created_local_time(self):
        return localtime(self.created)

