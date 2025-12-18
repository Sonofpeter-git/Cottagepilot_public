from django.test import TestCase
from sensors.models import Sensor
from accounts.models import CustomUser
from django.utils.timezone import now
from django.urls import reverse
from django.test import Client
from rest_framework.authtoken.models import Token

class testSensorViews(TestCase):
    def setUp(self):
        self.sensor_owner = CustomUser.objects.create_user(username="test_user", password="tikuri123", email="test@user.fi")
        self.sensor_owner.save()
        self.sensor1 = Sensor.objects.create(
            sensor_id="9f4c2e1d-8c5a-4e28-9b2c-3e13be0539a5", code="sensor_code", name="sensor1",
            type="temperature", unit="C", location="Kaaritie 4", description="Description?",
            status="active", owner=None, updated_at=now()
        )
        self.sensor1.save()
        self.client = Client()
        # Obtain auth token for the user
        token, created = Token.objects.get_or_create(user=self.sensor_owner)
        self.auth_header = {'HTTP_AUTHORIZATION': f'Token {token.key}'}

    def test_create_sensor(self):
        #tests the webflow when sensors post for the first time
        url = '/api/sensors/create_sensor/'
        data = {
            "sensor_id": "9f4c2e1d-8c9a-4e28-9b2c-3e13be0539a5"
        }

        response = self.client.post(url, data, content_type='application/json', **self.auth_header)
        self.sensor2 = Sensor.objects.get(sensor_id=data['sensor_id'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.sensor2.sensor_id, data['sensor_id'])

    def test_already_existing_sensor_creation(self):
        url = '/api/sensors/create_sensor/'
        data = {
            "sensor_id": "9f4c2e1d-8c5a-4e28-9b2c-3e13be0539a5"
        }

        response = self.client.post(url, data, content_type='application/json')
        self.sensor2 = Sensor.objects.get(sensor_id=data['sensor_id'])
        self.assertEqual(response.status_code, 200)


    def test_sensor_claim(self):
        url = '/api/sensors/claim_sensor/'
        data = {
            "sensor_id": "9f4c2e1d-8c5a-4e28-9b2c-3e13be0539a5",
            'unit' : 'c',
            'type' : 'temperature',
            'location' : 'Turku',
            'description' : 'ei oo'
        }
        response = self.client.post(url, data, content_type='application/json', **self.auth_header)
        self.sensor1 = Sensor.objects.get(sensor_id="9f4c2e1d-8c5a-4e28-9b2c-3e13be0539a5")
        self.assertEqual(response.status_code, 202)
        self.assertIn('success', response.json().get('status', ''))
        self.assertTrue(self.sensor1.is_sensor_claimed)
        self.assertEqual(self.sensor1.owner, self.sensor_owner)