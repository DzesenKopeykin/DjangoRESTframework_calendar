from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import Event, User
import datetime


class UserSerializer(serializers.HyperlinkedModelSerializer):
    country = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'country')
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.get_or_create(user=user)
        return user


class EventSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    end_time = serializers.TimeField(required=False)
    end_date = serializers.DateField(required=False)

    class Meta:
        model = Event
        fields = ('url', 'name', 'user', 'start_date', 'start_time', 'end_date', 'end_time', 'reminder_hours')
