from django.shortcuts import render
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from events.models import Event
from events.serializers import EventSerializer


class EventViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):

    permission_classes = (IsAuthenticated, )
    queryset = Event.objects.all()
    serializer_class = EventSerializer
