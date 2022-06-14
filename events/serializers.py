from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format='%m/%d/%Y %H:%M')
    end_time = serializers.DateTimeField(format='%m/%d/%Y %H:%M')

    class Meta:
        model = Event
        fields = ('title', 'description', 'start_time', 'end_time', )
