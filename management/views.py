import json

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from management.models import Item
from management.serializers import ItemSerializer


class ItemViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Item.objects.all()
        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data)
