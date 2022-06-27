from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format='%m/%d/%Y %H:%M', required=False, allow_null=True)
    end_time = serializers.DateTimeField(format='%m/%d/%Y %H:%M', required=False, allow_null=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'type', 'start_time', 'end_time', 'participants')
        read_only_fields = ('start_time', 'end_time')
