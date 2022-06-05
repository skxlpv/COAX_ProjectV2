from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from management.models import Item, Category
from management.serializers import ItemSerializer, CategorySerializer


class ItemViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """
    Item

    Item View Set
    """

    permission_classes = [IsAuthenticated, ]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def retrieve(self, request, *args, **kwargs):
        query_items = Item.objects.filter(name__istartswith=kwargs['pk'])
        serializer = ItemSerializer(query_items, many=True)
        return Response(serializer.data)


class CategoryViewSet(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    """
    Category

    Category View Set
    """

    permission_classes = [IsAuthenticated, ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        query_categories = Category.objects.filter(category_name__istartswith=kwargs['pk'])
        serializer = CategorySerializer(query_categories, many=True)
        return Response(serializer.data)
