from rest_framework import serializers
from ..models.team import Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = (
            "id",
            "user",
            "role",
            "project",
            "created_at",
            "updated_at"
        )