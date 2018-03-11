from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

from yourvoice.apps.messages.models import Message
from yourvoice.apps.issues.models import Issue, Stance

# Create your models here.
app_name = "filterers"

class FiltererToPolitician(models.Model):
    filterer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "politicians")
    politician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "filterers")
    accepted = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        if not self.filterer.is_filterer or not self.politician.is_politician:
            raise ValidationError("FiltererToPolitician must be between a filterer and a politician")
        super(FiltererToPolitician, self).save(*args, **kwargs)

class MessageTag(models.Model):
    filterer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    message = models.ForeignKey(Message, on_delete = models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete = models.CASCADE)
    stance = models.ForeignKey(Stance, on_delete = models.CASCADE)

