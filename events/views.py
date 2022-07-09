from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from events.models import Event
from events.serializers import EventSerializer


class EventViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    """
    list:
    List of events

    ### Here user get list of events from hospital, where user belong

    create:
    Event

    ### Create event. Title, Type and Participants(may be blank) of the event is required.

    read:
    Event

    ### Get detailed information about specific event by {id}.
    #### You should belong to the hospital, where this event is

    delete:
    Event

    ### Delete event, if user is the creator of event

    """

    permission_classes = (IsAuthenticated, )
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user, hospital=self.request.user.hospital)

    def get_queryset(self):
        return Event.objects.filter(hospital=self.request.user.hospital)
