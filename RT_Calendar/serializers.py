from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import Event


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.get_or_create(user=user)
        return user


class EventSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Event
        fields = ('url', 'name', 'user', 'start_datetime', 'end_datetime', 'reminder_hours')
