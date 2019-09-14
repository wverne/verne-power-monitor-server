import datetime
import pytz

from django.contrib.auth.models import User
from django.test import TestCase

from ..powerlog.models import PowerLog

from .models import Sensor


class DeleteSensorTestCase(TestCase):
    """
    A suite of tests covering the deletion of Sensors.
    """
    def setUp(self):
        """
        Create a test user.
        """
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass"
        )

    def test_delete_with_logs(self):
        """
        Ensure that when a Sensor with PowerLogs is deleted, its PowerLogs are
        deleted as well.
        """
        # Create two test sensors
        sensor_to_delete = Sensor.objects.create(
            name="Sensor To Delete",
            created_at=datetime.datetime(2018, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        )
        sensor_to_leave_in_place = Sensor.objects.create(
            name="Sensor To Leave In Place",
            created_at=datetime.datetime(2018, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        )

        # Create two logs each for the test sensors
        PowerLog.objects.create(
            timestamp=datetime.datetime(2018, 1, 1, 0, 0, 0, tzinfo=pytz.UTC),
            network_ssid='TestWifiNetwork',
            network_local_ip='10.0.0.123',
            sensor=sensor_to_delete
        )
        PowerLog.objects.create(
            timestamp=datetime.datetime(2018, 1, 1, 2, 0, 0, tzinfo=pytz.UTC),
            network_ssid='TestWifiNetwork',
            network_local_ip='10.0.0.123',
            sensor=sensor_to_delete
        )
        PowerLog.objects.create(
            timestamp=datetime.datetime(2018, 1, 1, 0, 0, 0, tzinfo=pytz.UTC),
            network_ssid='TestWifiNetwork',
            network_local_ip='10.0.0.124',
            sensor=sensor_to_leave_in_place
        )
        PowerLog.objects.create(
            timestamp=datetime.datetime(2018, 1, 1, 2, 0, 0, tzinfo=pytz.UTC),
            network_ssid='TestWifiNetwork',
            network_local_ip='10.0.0.124',
            sensor=sensor_to_leave_in_place
        )

        self.client.force_login(self.user)
        response = self.client.post(
            '/sensors/delete/{}/'.format(sensor_to_delete.id)
        )

        # Response should be a redirect to the sensors list
        self.assertEqual(302, response.status_code)

        # Ensure that the chosen sensor and its logs were deleted
        self.assertFalse(
            Sensor.objects.filter(id=sensor_to_delete.id).exists()
        )
        self.assertFalse(
            PowerLog.objects.filter(sensor_id=sensor_to_delete.id).exists()
        )

        # Ensure that the other sensor and its logs were not affected
        self.assertTrue(
            Sensor.objects.filter(id=sensor_to_leave_in_place.id).exists()
        )
        self.assertEqual(
            2,
            PowerLog.objects.filter(sensor_id=sensor_to_leave_in_place.id)
                            .count()
        )

    def test_delete_no_logs(self):
        """
        Ensure that a Sensor with no PowerLogs may be deleted.
        """
        sensor_to_delete = Sensor.objects.create(
            name="Sensor To Delete",
            created_at=datetime.datetime(2018, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        )

        self.client.force_login(self.user)
        response = self.client.post(
            '/sensors/delete/{}/'.format(sensor_to_delete.id)
        )

        # Response should be a redirect to the sensors list
        self.assertEqual(302, response.status_code)

        # Ensure that the chosen sensor was deleted
        self.assertFalse(
            Sensor.objects.filter(id=sensor_to_delete.id).exists()
        )

    def test_delete_no_auth(self):
        """
        Ensure that a Sensor may not be deleted by an unauthenticated user.
        """
        sensor_to_delete = Sensor.objects.create(
            name="Sensor To Delete",
            created_at=datetime.datetime(2018, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        )

        response = self.client.post(
            '/sensors/delete/{}/'.format(sensor_to_delete.id)
        )

        # Response should be a redirect to the login page
        self.assertEqual(302, response.status_code)

        # Ensure that the chosen sensor was *not* deleted
        self.assertTrue(Sensor.objects.filter(id=sensor_to_delete.id).exists())

    def test_delete_nonexistent_sensor(self):
        """
        Ensure that attempting to delete a nonexistent Sensor results in a 404.
        """
        self.client.force_login(self.user)
        response = self.client.post('/sensors/delete/123/')

        self.assertEqual(404, response.status_code)
