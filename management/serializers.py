from rest_framework import serializers
from rest_framework.fields import Field

from management.models import Item, Category

Field.default_error_messages = {
    'required': 'This field is required',
}


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'hospital', 'name', 'category',
                  'description', 'quantity', 'price_of_one',)
        extra_kwargs = {
            'quantity': {'required': True},
            'price_of_one': {'required': True}
        }

    def update(self, item, validated_data):
        quantity = self.validated_data.get('quantity')
        if not quantity:
            raise serializers.ValidationError('No quantity of item was given')

        item.quantity = validated_data['quantity']
        item.save()
        return item


class CategorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ('id', 'hospital', 'items')
