import rest_framework.serializers as serializer
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.mail import send_mail
from twitter import Twitter, OAuth

from core.models import Message, Notification


class MessageSerializerList(serializer.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'topic', 'updated']


class MessageSerializerDetail(serializer.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receivers', 'responses', 'content']

    def send(self, obj):
        send_mail(
            obj.topic,
            obj.content,
            obj.sender.email,
            obj.receivers.values('email'),
            fail_silently=False,
        )

    def send_pm_in_tweet(self, obj):
        birdy = Twitter(auth=OAuth(settings.TWITTER_TOKEN, settings.TWITTER_TOKEN_SECRET, settings.TWITTER_CONSUMER_KEY,
                                   settings.TWITTER_CONSUMER_SECRET))
        for receiver in obj.receivers:
            receiver_id = birdy.users.show(screen_name=receiver.twitter_id)["id"]
            notification_msg = Notification.objetcs.get(service_name='twitter').content
            twt_pm = """{
                    "event": {
                        "type": "message_create",
                        "message_create": {
                            "target": {
                                "recipient_id": {0}
                            },
                            "message_data": {
                                "text": {1}
                            }
                        }
                    }
            }""".format(receiver_id, notification_msg)
            birdy.direct_messages.events.new(_json=twt_pm)


class MessageSerializerCreate(serializer.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'receivers', 'topic', 'content']

        def validate_sender(self, obj):
            if obj.sender.total_strikes >= settings.MAX_TOTAL_STRIKES:
                raise ValidationError(("Blacklisted User"), params={"user": obj.id})
