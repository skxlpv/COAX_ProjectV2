from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from management.models import Item, Category
from management.serializers import ItemSerializer, CategorySerializer


class ItemViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):

    permission_classes = [IsAuthenticated, ]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class CategoryViewSet(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):

    permission_classes = [IsAuthenticated, ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
