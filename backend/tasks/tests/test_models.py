from django.test import TestCase
from tasks.models import Task
from tasks.serializers import TaskSerializer

class test_task_model(TestCase):
  def setUp(self):
    self.task1 = Task.objects.create(name="test_task1", group="test", location="alal mösä", description="do something")
    self.task2 = Task.objects.create(name="test_task2", group="test", location="yläl mösä", description="do something")

  def test_get_tasks_in_group(self):
    tasks = self.task1.get_tasks_in_group('test')
    serialized = TaskSerializer(tasks, many=True)
    task_names = [task_data['name'] for task_data in serialized.data]
    self.assertEqual(task_names, ['test_task2', 'test_task1'])