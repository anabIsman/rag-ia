from rest_framework import serializers

from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "id",
            "file",
            "original_filename",
            "status",
            "failure_reason",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["status", "failure_reason", "created_at", "updated_at"]
