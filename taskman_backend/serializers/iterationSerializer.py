from rest_framework import serializers
from ..models.iteration import Iteration

class IterationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Iteration
        fields = (
            "id",
            "project",
            "version",
            "title",
            "description",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
            "updated_by"
        )