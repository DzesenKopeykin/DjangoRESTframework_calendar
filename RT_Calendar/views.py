from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework import viewsets
from django.contrib.auth.models import User

from .serializers import UserSerializer


class UserViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
