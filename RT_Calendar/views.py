from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer, EventSerializer
from .models import Event


class UserViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
