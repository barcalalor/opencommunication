from django.db import models

# Masters
from authentification.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='message_sender', null=True)
    receivers = models.ManyToManyField(User, related_name="message_receivers")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    responses = models.ManyToManyField("self")
    topic = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        unique_together = (("id", "sender"),)
