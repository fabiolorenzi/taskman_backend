from rest_framework import serializers
from ..models.project import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model: Project
        fields = (
            "id",
            "name",
            "description",
            "main_user",
            "created_at",
            "updated_at"
        )