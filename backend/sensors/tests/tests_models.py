from django.test import TestCase
from sensors.models import Sensor
from accounts.models import CustomUser
from datetime import timedelta
from django.utils.timezone import now
# Create your tests here.
class testSensorModels(TestCase):
  @classmethod
  def setUpTestData(cls):
    owner = CustomUser.objects.create(username="test_user", password="tikuri123", email="test@user.fi")
    sensor1 = Sensor.objects.create(id="9f4c2e1d-8c5a-4e28-9b2c-3e13be0539a5", code="sensor_code", name="sensor1",
                                        type="temperature", unit="C", location="Kaaritie 4", description="Description?"
                                      , status="active", owner=owner, updated_at=now)
    sensor1.save()

  def test_sensor_update_last_reading(self):
    self.sensor1 = Sensor.objects.get(name="sensor1")
    self.sensor1.update_last_reading(2.1)
    return self.assertEqual(self.sensor1.last_reading, 2.1)
  
  
  def test_is_sensor_claimed(self):
    self.sensor1 = Sensor.objects.get(name="sensor1")
    self.assertTrue(self.sensor1.is_sensor_claimed)
    user = self.sensor1.owner
    self.sensor1.owner = None
    self.assertFalse(self.sensor1.is_sensor_claimed)
    self.sensor1.owner = user
    self.sensor1.save()



  def test_sensor_status(self):
    #test both scenes if sensor updated_at was more than 2 hours ago and
    #less than 2 hours ago
    self.sensor1 = Sensor.objects.get(name="sensor1")
    self.assertEqual(self.sensor1.sensor_status, 'active')
    self.sensor1.updated_at = now()-timedelta(hours=3)
    self.assertEqual(self.sensor1.sensor_status, 'inactive')
