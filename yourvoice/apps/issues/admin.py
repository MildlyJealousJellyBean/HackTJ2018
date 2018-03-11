from django.contrib import admin

from .models import Issue, Stance

# Register your models here.
admin.site.register(Issue)
admin.site.register(Stance)
