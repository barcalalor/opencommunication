import rest_framework.serializers as serializer
from django.core.exceptions import ValidationError
from django.conf import settings

from core.models import Message


class MessageSerializerList(serializer.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'topic', 'updated']


class MessageSerializerDetail(serializer.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receivers', 'responses', 'content']


class MessageSerializerCreate(serializer.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'receivers', 'topic', 'content']

        def validate_sender(self, obj):
            if obj.sender.total_strikes > settings.MAX_TOTAL_STRIKES:
                raise ValidationError(("Blacklisted User"), params={"user": obj.id})
