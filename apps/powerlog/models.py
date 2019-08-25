from django.db import models


class PowerLog(models.Model):
    """
    Represents a log received from the power monitor device.
    """
    timestamp = models.DateTimeField()
    network_ssid = models.CharField(max_length=127)
    network_local_ip = models.GenericIPAddressField(protocol="IPv4")
    sensor = models.ForeignKey('sensor.Sensor', on_delete=models.PROTECT)
