from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from management.models import Item, Category
from management.serializers import ItemSerializer, CategorySerializer


class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
