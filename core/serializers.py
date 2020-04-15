from rest_framework import serializers


class ApplicationEditSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    key = serializers.CharField(max_length=255)


class ApplicationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
