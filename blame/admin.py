""" Django administrative panel view registrations """

from django.contrib import admin
from . import models


@admin.register(models.Blame)
class BlameAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'username', 'created_at']
