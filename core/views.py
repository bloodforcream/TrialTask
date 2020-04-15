from uuid import uuid4

from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Application
from core.serializers import ApplicationSerializer, ApplicationEditSerializer


class ApplicationAllowedToUser(permissions.BasePermission):
    @staticmethod
    def check_permission(user, obj):
        if user in obj.users.all():
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return self.check_permission(request.user, obj)


class ApplicationView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get_application(request, request_type='GET'):
        data = request.GET if request_type == 'GET' else request.POST

        if 'key' not in data:
            return None, Response({'status': 400, 'errors': 'Не указан ключ'}, status=status.HTTP_400_BAD_REQUEST)

        key = data['key']
        try:
            app = Application.objects.get(key=key)
        except Application.DoesNotExist:
            return None, Response({'status': 404, 'errors': 'Приложение с таким ключем не существует'},
                                  status=status.HTTP_404_NOT_FOUND)

        return app, None

    def retrieve(self, request, *args, **kwargs):
        app, error_resp = self.get_application(request)
        if error_resp:
            return error_resp

        if not ApplicationAllowedToUser.check_permission(request.user, app):
            return Response({'status': 400, 'errors': 'У вас нет доступа к данному приложению'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'name': app.name}, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            key = str(uuid4())
            new_app = Application.objects.create(name=serializer.validated_data['name'], key=key)
            new_app.users.add(request.user)
        else:
            return Response({'status': 400, 'errors': 'Неверные данные'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'name': new_app.name, 'key': new_app.key}, status=status.HTTP_200_OK)

    def update(self, request):
        serializer = ApplicationEditSerializer(data=request.data)
        if serializer.is_valid():
            try:
                app = Application.objects.get(key=serializer.validated_data['key'])
                if ApplicationAllowedToUser.check_permission(request.user, app):
                    app.name = serializer.validated_data['name']
                    app.save()
                else:
                    return Response({'status': 400, 'errors': 'У вас нет доступа к данному приложению'},
                                    status=status.HTTP_400_BAD_REQUEST)

            except Application.DoesNotExist:
                return Response({'status': 404, 'errors': 'Приложение с таким ключем не существует'},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'status': 400, 'errors': 'Неверные данные'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'name': app.name, 'key': app.key}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        app, error_resp = self.get_application(request, request_type='POST')
        if error_resp:
            return error_resp

        if ApplicationAllowedToUser.check_permission(request.user, app):
            app.delete()
        else:
            return Response({'status': 400, 'errors': 'У вас нет доступа к данному приложению'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'ok'}, status=status.HTTP_200_OK)
