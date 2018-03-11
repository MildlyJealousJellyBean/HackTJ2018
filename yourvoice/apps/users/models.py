from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

from yourvoice.apps.filterers.models import FiltererToPolitician

app_name = "users"

class User(AbstractUser):
    USER_TYPES = (
        ('person', 'Normal user'),
        ('filterer', 'Filterer'),
        ('politician', 'Politician'),
    )
    user_type = models.CharField(max_length = 20, choices = USER_TYPES, default = USER_TYPES[0][0])

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    @property
    def is_normal_user(self):
        return self.user_type == "person"

    @property
    def is_filterer(self):
        return self.user_type == "filterer"
        
    @property
    def is_politician(self):
        return self.user_type == "politician"
    
    @property
    def politicians_filtered(self):
        return [ftp.politician for ftp in FiltererToPolitician.objects.filter(filterer = self) if ftp.accepted]
    
    @property
    def politician_filter_requests(self):
        return [ftp.politician for ftp in FiltererToPolitician.objects.filter(filterer = self) if not ftp.accepted]

    @property
    def connected_filterers(self):
        return [ftp.filterer for ftp in FiltererToPolitician.objects.filter(politician = self) if ftp.accepted]
    @property
    def requested_filterers(self):
        return [ftp.filterer for ftp in FiltererToPolitician.objects.filter(politician = self) if not ftp.accepted]
    
    def connect_to_politician(self, politician):
        if not self.is_filterer:
            raise TypeError("Non-filterer cannot connect to politician")
        try:
            ftp = FiltererToPolitician.objects.get(filterer = self, politician = politician, accepted = False)
        except FiltererToPolitician.DoesNotExist:
            pass
        else:
            ftp.accepted = True
            ftp.save()

    def disconnect_from_politician(self, politician):
        try:
            ftp = FiltererToPolitician.objects.get(filterer = self, politician = politician)
        except FiltererToPolitician.DoesNotExist:
            pass
        else:
            ftp.delete()

            
    def connect_to_filterer(self, filterer):
        if not self.is_politician:
            raise TypeError("Non-politician cannot connect to filterer")
        if not list(FiltererToPolitician.objects.filter(filterer = filterer, politician = self)):
            ftp = FiltererToPolitician(filterer = filterer, politician = self)
            ftp.save()

    def disconnect_from_filterer(self, filterer):
        try:
            ftp = FiltererToPolitician.objects.get(filterer = filterer, politician = self)
        except FiltererToPolitician.DoesNotExist:
            pass
        else:
            ftp.delete()
    
    def is_connected_to_politician(self, politician):
        try:
            ftp = FiltererToPolitician.objects.get(filterer = self, politician = politician, accepted = True)
            return True
        except FiltererToPolitician.DoesNotExist:
            return False

    def is_connected_to_filterer(self, filterer):
        try:
            ftp = FiltererToPolitician.objects.get(filterer = filterer, politician = self, accepted = True)
            return True
        except FiltererToPolitician.DoesNotExist:
            return False
    
    def has_request_from(self, politician):
        try:
            ftp = FiltererToPolitician.objects.get(filterer = self, politician = politician, accepted = False)
            return True
        except FiltererToPolitician.DoesNotExist:
            return False

    def has_requested(self, filterer):
        try:
            ftp = FiltererToPolitician.objects.get(filterer = filterer, politician = self, accepted = False)
            return True
        except FiltererToPolitician.DoesNotExist:
            return False

