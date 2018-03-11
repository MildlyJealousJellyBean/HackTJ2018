from django.db import models

# Create your models here.

class Issue(models.Model):
    name = models.CharField(max_length = 100)
    @property
    def stances(self):
        return list(Stance.objects.filter(issue = self))
    def __str__(self):
        return self.name

class Stance(models.Model):
    issue = models.ForeignKey(Issue, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100)
    def __str__(self):
        return self.name
