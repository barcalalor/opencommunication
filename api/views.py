from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
import api.serializers as serializers
from core.models import Message


class MessageViewSet(viewsets.ModelViewSet):

    def get_queryset(self, request):
        return Message.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.MessageSerializerList
        if self.action == "retrieve":
            return serializers.MessageSerializerDetail
        if self.action == "create":
            return serializers.MessageSerializerCreate