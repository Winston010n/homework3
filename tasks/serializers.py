from django.utils import timezone
from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "due_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Название задачи должно содержать не менее 5 символов."
            )
        if value.isdigit():
            raise serializers.ValidationError(
                "Название задачи не может состоять только из цифр."
            )
        return value

    def validate_priority(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError(
                "Приоритет должен быть в диапазоне от 1 до 5."
            )
        return value

    def validate(self, attrs):
        due_date = attrs.get("due_date")
        if due_date is not None and due_date < timezone.now():
            raise serializers.ValidationError(
                {"due_date": "Дедлайн не может быть в прошлом."}
            )
        return attrs