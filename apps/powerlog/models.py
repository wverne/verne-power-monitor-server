from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class PowerLog(models.Model):
    """
    Represents a log received from the power monitor device.
    """
    timestamp = models.DateTimeField()
    # The SSID of the WiFi network to which the sensor was connected.
    network_ssid = models.CharField(max_length=127)
    # The local IP address of the sensor.
    network_local_ip = models.GenericIPAddressField(protocol="IPv4")
    sensor = models.ForeignKey('sensor.Sensor', on_delete=models.PROTECT)


@receiver(post_save, sender=PowerLog)
def update_sensor_denormalized_log_fields(sender, instance, **kwargs):
    """
    After a PowerLog is saved, update its Sensor's denormalized log fields.
    """
    instance.sensor.latest_network_ssid = instance.network_ssid
    instance.sensor.latest_network_local_ip = instance.network_local_ip
    instance.sensor.save()
