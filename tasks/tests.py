from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task


class TaskApiTests(APITestCase):
    def setUp(self):
        self.list_url = reverse("task-list")
        self.valid_data = {
            "title": "Подготовить отчет",
            "description": "Краткое описание",
        }

    def test_create_and_list_tasks(self):
        create_response = self.client.post(
            self.list_url, self.valid_data, format="json"
        )

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_response.data["status"], Task.Status.PENDING)
        self.assertEqual(create_response.data["priority"], 3)
        self.assertIn("created_at", create_response.data)

        list_response = self.client.get(self.list_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)

    def test_invalid_title_is_rejected(self):
        for title in ("abc", "12345"):
            with self.subTest(title=title):
                response = self.client.post(
                    self.list_url,
                    {**self.valid_data, "title": title},
                    format="json",
                )
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn("title", response.data)

    def test_priority_outside_range_is_rejected(self):
        response = self.client.post(
            self.list_url,
            {**self.valid_data, "priority": 6},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("priority", response.data)

    def test_past_due_date_is_rejected(self):
        past_date = (timezone.now() - timedelta(days=1)).isoformat()
        response = self.client.post(
            self.list_url,
            {**self.valid_data, "due_date": past_date},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("due_date", response.data)

    def test_retrieve_update_and_delete_task(self):
        task = Task.objects.create(title="Подготовить отчет")
        detail_url = reverse("task-detail", args=[task.pk])

        self.assertEqual(self.client.get(detail_url).status_code, status.HTTP_200_OK)
        patch_response = self.client.patch(
            detail_url, {"status": Task.Status.COMPLETED}, format="json"
        )
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.data["status"], Task.Status.COMPLETED)

        delete_response = self.client.delete(detail_url)
        self.assertEqual(
            delete_response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())