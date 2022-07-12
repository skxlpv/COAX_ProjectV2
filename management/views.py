from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from core.pagination import StandardResults, SmallResults
from management.models import Item, Category
from management.serializers import CategorySerializer, ItemSerializer


class ItemViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    """
    list:
    List of Items

    ### Here user get list of items from hospital, where user belong

    create:
    Item

    ### Create new item, by giving name, hospital, category and quantity.
    Hospital will be taken automatically

    read:
    Single item

    ### Get detailed information about specific item by {id}.
    #### You should belong to the hospital, where this item is

    update:
    Item

    ### User must belong to this hospital

    partial_update:
    Item

    ### User must belong to this hospital

    delete:
    Delete item

    ### Delete item, if user belong to the hospital

    """

    permission_classes = [IsAuthenticated, ]
    serializer_class = ItemSerializer
    pagination_class = StandardResults

    def perform_create(self, serializer):
        serializer.save(hospital=self.request.user.hospital)

    def get_queryset(self):
        return Item.objects.all().filter(hospital=self.request.user.hospital)


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    """
    list:
    List of categories

    ### Get list of all the categories of current hospital

    read:
    Single category

    ### Get detailed information about specific category by {id}.
    #### You should belong to the hospital, where this category is

    """

    permission_classes = [IsAuthenticated, ]
    serializer_class = CategorySerializer
    pagination_class = SmallResults

    def get_queryset(self):
        return Category.objects.all().filter(hospital=self.request.user.hospital)
