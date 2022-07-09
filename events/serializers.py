from rest_framework import serializers

from events.models import Event
from hospitals.serializers import HospitalSerializer
from users.serializers import AuthorSerializer


class EventSerializer(serializers.ModelSerializer):
    creator = AuthorSerializer(read_only=True)
    hospital = HospitalSerializer(read_only=True)
    start_time = serializers.DateTimeField(format='%m/%d/%Y %H:%M', required=False, allow_null=True)
    end_time = serializers.DateTimeField(format='%m/%d/%Y %H:%M', required=False, allow_null=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'type',
                  'start_time', 'end_time', 'participants',
                  'creator', 'hospital')
        read_only_fields = ('start_time', 'end_time')
