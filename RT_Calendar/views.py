from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework import viewsets
from .serializers import UserSerializer, EventSerializer
from .models import Event, User
from datetime import datetime, time, timedelta


class UserViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        print(self.request.data)
        serializer.save(user=self.request.user,
                        end_date=self.request.data['end_date']
                            if 'end_date' in self.request.data else self.request.data['start_date'],
                        end_time=self.request.data['end_time'] if 'end_time' in self.request.data else time(23, 59)
                        )

    def get_queryset(self):
        queryset = Event.objects.filter(user=self.request.user)
        if 'day' in self.request.data:
            queryset = queryset.filter(start_date=datetime.strptime(self.request.data['day'], '%Y-%m-%d'))
        elif 'month' in self.request.data:
            date1 = datetime.strptime(self.request.data['month'], '%Y-%m')
            date2 = datetime(date1.year, date1.month + 1, date1.day)
            queryset = queryset.filter(start_date__range=[date1, date2])
        return queryset
