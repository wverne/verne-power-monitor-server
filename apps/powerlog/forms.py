from django.forms import ModelForm

from .models import PowerLog


class PowerLogForm(ModelForm):
    class Meta:
        model = PowerLog
        fields = ['sensor', 'network_ssid', 'network_local_ip']
