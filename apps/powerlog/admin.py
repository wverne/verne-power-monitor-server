from django.contrib import admin

from . import models


@admin.register(models.PowerLog)
class PowerLogAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp',
        'sensor',
        'network_ssid',
        'network_local_ip'
    )
    ordering = ('-timestamp',)
