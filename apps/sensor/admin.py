from django.contrib import admin

from . import models


@admin.register(models.Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_at'
    )
    ordering = ('name',)
