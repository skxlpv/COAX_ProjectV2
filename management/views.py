from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.pagination import SmallResults, StandardResults
from management.models import Item, Category
from management.serializers import ItemSerializer, CategorySerializer


class ItemViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.CreateModelMixin,
                  GenericViewSet):
    """
    Item
    """

    permission_classes = [IsAuthenticated, ]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = SmallResults

    def retrieve(self, request, *args, **kwargs):
        query_items = Item.objects.filter(name__istartswith=kwargs['pk'])
        serializer = ItemSerializer(query_items, many=True)
        return Response(serializer.data)


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    """
    Category
    """

    permission_classes = [IsAuthenticated, ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResults

    # def retrieve(self, request, *args, **kwargs):
    #     query_categories = Category.objects.filter(category_name__istartswith=kwargs['pk'])
    #     serializer = CategorySerializer(query_categories, many=True)
    #     return Response(serializer.data)
