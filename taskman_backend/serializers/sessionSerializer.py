from rest_framework import serializers
from ..models.session import Session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = (
            "id",
            "user",
            "passcode",
            "expire"
        )