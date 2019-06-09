from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from RT_Calendar.views import HelloView

urlpatterns = [
    path('hello/', HelloView.as_view(), name='hello'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('admin/', admin.site.urls),
]
