from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from core.views import ApplicationView

urlpatterns = [
    path('api/auth/', obtain_auth_token, name='auth'),
    path('api/test/', ApplicationView.as_view({'get': 'retrieve'}), name='application-retrieve'),

    path('api/test/create/', ApplicationView.as_view({'post': 'create'}), name='application-create'),
    path('api/test/update/', ApplicationView.as_view({'post': 'update'}), name='application-update'),
    path('api/test/delete/', ApplicationView.as_view({'post': 'destroy'}), name='application-destroy'),
    path('api/test/change_key/', ApplicationView.as_view({'post': 'change_key'}), name='application-change-key'),
]
