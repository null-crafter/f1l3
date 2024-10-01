from rest_framework.serializers import ModelSerializer

from core.models import UploadedFile


class UploadedFileSerializer(ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ["id", "file"]
