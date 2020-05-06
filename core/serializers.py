from rest_framework import serializers, status
from core.models import Application


class ApplicationSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=255)

    def get_instance(self):
        instance = Application.objects.get(key=self.validated_data['key'])
        return instance


class ApplicationUpdateSerializer(ApplicationSerializer):
    name = serializers.CharField(max_length=255)


class ApplicationCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
