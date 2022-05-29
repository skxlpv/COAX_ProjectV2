import json

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from management.models import Item
from management.serializers import ItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def partial_update(self, request, *args, **kwargs):
        item_ser = self.get_serializer(Item, data=request.data, partial=True)
        item_ser.save()