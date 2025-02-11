from rest_framework import serializers
from ..models.task import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "number",
            "title",
            "description",
            "type",
            "priority",
            "status",
            "project",
            "user",
            "iteration",
            "created_at",
            "updated_at",
            "updated_by"
        )