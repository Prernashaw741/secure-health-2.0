from rest_framework.serializers import ModelSerializer

from management.models import Uploads, tests

class UploadSerializer(ModelSerializer):
    class Meta:
        model = Uploads
        fields = "__all__"

class TESTSerializer(ModelSerializer):
    class Meta:
        model = tests
        fields = "__all__"
        