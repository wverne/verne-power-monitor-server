import datetime
import pytz

from django.test import TestCase

from ..sensor.models import Sensor

from .models import PowerLog


class DenormalizedSensorLogFieldsTestCase(TestCase):
    """
    A suite of tests concerning the denormalized log fields on the Sensor
    model.
    """
    def test_fields_updated_on_log_create(self):
        """
        Ensure that the Sensor denormalized log fields are updated when a
        PowerLog is created.
        """
        # Create two test sensors
        sensor_to_log = Sensor.objects.create(
            name="Sensor To Log",
            created_at=datetime.datetime(2018, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        )
        sensor_not_to_log = Sensor.objects.create(
            name="Sensor Not To Log",
            created_at=datetime.datetime(2018, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        )

        # Create the log
        test_ssid = 'TestWifiNetwork'
        test_ip = '10.0.0.123'
        PowerLog.objects.create(
            timestamp=datetime.datetime(2018, 1, 1, 0, 0, 0, tzinfo=pytz.UTC),
            network_ssid=test_ssid,
            network_local_ip=test_ip,
            sensor=sensor_to_log
        )

        # Ensure the correct sensor was updated
        sensor_to_log.refresh_from_db()
        self.assertEqual(test_ssid, sensor_to_log.latest_network_ssid)
        self.assertEqual(test_ip, sensor_to_log.latest_network_local_ip)

        # Ensure the other sensor was not updated
        sensor_not_to_log.refresh_from_db()
        self.assertIsNone(sensor_not_to_log.latest_network_ssid)
        self.assertIsNone(sensor_not_to_log.latest_network_local_ip)
