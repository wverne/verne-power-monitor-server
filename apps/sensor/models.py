from django.db import models


class Sensor(models.Model):
    """
    Represents a power monitor device.
    """
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.name
