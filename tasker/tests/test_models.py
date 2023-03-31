from django.test import TestCase

from tasker.models import Tag, Task


class ModelTests(TestCase):
    def test_tag_str(self):
        tag = Tag.objects.create(
            name="test"
        )

        self.assertEqual(
            str(tag),
            tag.name
        )

    def test_task_str(self):
        task = Task.objects.create(
            content="test",
        )

        self.assertEqual(
            str(task),
            task.content
        )
