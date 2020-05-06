from uuid import uuid4

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Application
from core.serializers import ApplicationCreateSerializer, ApplicationSerializer, ApplicationUpdateSerializer


class ApplicationView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def get_app_validation(self, serializer):
        if serializer.is_valid():
            try:
                serializer.get_instance()
            except ObjectDoesNotExist:
                return Response({'status': 404, 'errors': 'Приложение с таким ключем не существует'},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'status': 400, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        serializer = ApplicationSerializer(data=request.GET)
        error_response = self.get_app_validation(serializer)
        if error_response:
            return error_response
        else:
            instance = serializer.get_instance()
        return Response({'name': instance.name}, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = ApplicationCreateSerializer(data=request.data)
        if serializer.is_valid():
            key = str(uuid4())
            new_app = Application.objects.create(name=serializer.validated_data['name'], key=key)
        else:
            return Response({'status': 400, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'name': new_app.name, 'key': new_app.key}, status=status.HTTP_200_OK)

    def update(self, request):
        serializer = ApplicationUpdateSerializer(data=request.data)
        error_response = self.get_app_validation(serializer)
        if error_response:
            return error_response
        else:
            instance = serializer.get_instance()
            instance.name = serializer.validated_data['name']
            instance.save()
        return Response({'name': instance.name, 'key': instance.key}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        serializer = ApplicationSerializer(data=request.data)
        error_response = self.get_app_validation(serializer)
        if error_response:
            return error_response
        else:
            instance = serializer.get_instance()
            instance.delete()
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

    def change_key(self, request, *args, **kwargs):
        serializer = ApplicationSerializer(data=request.data)
        error_response = self.get_app_validation(serializer)
        if error_response:
            return error_response
        else:
            instance = serializer.get_instance()
            instance.regenerate_key()
        return Response({'name': instance.name, 'key': instance.key}, status=status.HTTP_200_OK)
