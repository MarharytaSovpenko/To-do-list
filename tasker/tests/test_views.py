from django.urls import reverse
from django.test import TestCase
from tasker.models import Tag, Task

TAG_LIST_URL = reverse("tasker:tag-list")
TASK_LIST_URL = reverse("tasker:task-list")


class TagTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Test Tag")

    def test_tag_list_view(self):
        response = self.client.get(TAG_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasker/tag_list.html")

    def test_tag_create_view(self):
        response = self.client.post(
            reverse("tasker:tag-create"), {"name": "New Tag"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, TAG_LIST_URL)
        self.assertTrue(Tag.objects.filter(name="New Tag").exists())

    def test_tag_update_view(self):
        response = self.client.post(
            reverse("tasker:tag-update", args=[self.tag.pk]),
            {"name": "Updated Tag"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, TAG_LIST_URL)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, "Updated Tag")

    def test_tag_delete_view(self):
        response = self.client.post(
            reverse("tasker:tag-delete", args=[self.tag.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, TAG_LIST_URL)
        self.assertFalse(Tag.objects.filter(pk=self.tag.pk).exists())


class TaskTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Tag")
        self.task = Task.objects.create(
            content="Test Task", deadline="2023-05-01", done=False
        )
        self.task.task_tag.add(self.tag)
        self.form_data = {
            "content": "Task",
            "deadline": "2023-05-02",
            "done": True,
            "task_tag": [self.tag.pk],
        }

    def test_task_list_view(self):
        response = self.client.get(TASK_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasker/task_list.html")

    def test_task_list_ordered_by_created_time_and_tag_done(self):
        response = self.client.get(TASK_LIST_URL)
        task_list = Task.objects.order_by("done", "-time_creation")
        task_context = response.context["task_list"]

        self.assertEqual(
            list(task_context),
            list(task_list[: len(task_context)]),
        )

    def test_task_create_view(self):
        response = self.client.post(
            reverse("tasker:task-create"), self.form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, TASK_LIST_URL)
        self.assertTrue(Task.objects.filter(content="Task").exists())

    def test_task_update_view(self):
        response = self.client.post(
            reverse("tasker:task-update", args=[self.task.pk]), self.form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, TASK_LIST_URL)
        self.task.refresh_from_db()
        self.assertEqual(self.task.content, "Task")
        self.assertEqual(self.task.deadline.strftime("%Y-%m-%d"), "2023-05-02")
        self.assertTrue(self.task.done)
        self.assertTrue(self.task.task_tag.filter(name="Tag").exists())

    def test_task_delete_view(self):
        response = self.client.post(
            reverse("tasker:task-delete", args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, TASK_LIST_URL)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_toggle_done(self):
        response = self.client.get(
            reverse("tasker:toggle-done", kwargs={"pk": self.task.pk})
        )
        self.task.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, TASK_LIST_URL)
        self.assertTrue(self.task.done)

    def test_toggle_not_done(self):
        self.task.done = True
        self.task.save()
        response = self.client.get(
            reverse("tasker:toggle-done", kwargs={"pk": self.task.pk})
        )
        self.task.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, TASK_LIST_URL)
        self.assertFalse(self.task.done)
