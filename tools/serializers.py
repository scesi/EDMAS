from rest_framework import serializers
from .models import ScanJob

class ScanJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanJob
        fields = ['id', 'target', 'state', 'created_at', 'started_at', 'finished_at', 'subdomains', 'raw_output']

class ScanCreateSerializer(serializers.Serializer):
    target = serializers.CharField(max_length=255)
