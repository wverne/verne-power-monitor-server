from django.db import models


class Sensor(models.Model):
    """
    Represents a power monitor device.
    """
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    # The SSID of the WiFi network to which the sensor was connected, as of its last log. This is a denormalized field
    # and should reflect the network_ssid value of the latest PowerLog from this sensor.
    latest_network_ssid = models.CharField(max_length=127, null=True, default=None)
    # The local IP address of the sensor, as of its last log. This is a denormalized field and should reflect the
    # network_local_ip value of the latest PowerLog from this sensor.
    latest_network_local_ip = models.GenericIPAddressField(protocol="IPv4", null=True, default=None)

    def __str__(self):
        return self.name
