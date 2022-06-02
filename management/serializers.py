from rest_framework import serializers

from management.models import Item, Category


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'category_name', 'name',
                  'description', 'quantity', 'price_of_one')
        read_only_fields = ('category_name',)

    def update(self, instance, validated_data):
        instance.quantity = validated_data['quantity']
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ('id', 'category_name', 'department', 'items')

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.save()
        return instance
