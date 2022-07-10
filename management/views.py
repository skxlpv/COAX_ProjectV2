from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from core.pagination import SmallResults, StandardResults
from management.models import Item, Category
from management.serializers import ItemSerializer, CategorySerializer


class ItemViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    """
    list:

    Item List

    GET list of all the items

    retrieve:

    Item Detail

    GET detailed view of a single item

    destroy:

    Item Destroy

    DELETEs a single item

    update:

    Item Update

    PUT item's quantity field only...¯|_ (ツ) _/¯

    partial_update:

    Item Patch

    PATCH item's quantity field only

    create:

    Item Create

    POST item
    """

    permission_classes = [IsAuthenticated, ]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = SmallResults


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    """
    list:

    Category List

    GET list of all the categories

    retrieve:

    Category Detail

    GET detailed view of a single category
    """

    permission_classes = [IsAuthenticated, ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResults

