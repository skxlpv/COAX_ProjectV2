from rest_framework import serializers

from management.models import Item, Category


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'category_name', 'name',
                  'description', 'quantity', 'price_of_one')
        read_only_fields = ('category_name', 'name',
                            'description', 'price_of_one')

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
        fields = ('id', 'category_name', 'department', 'items')
        read_only_fields = ('department', 'items')

    def update(self, category, validated_data):
        category_name = self.validated_data.get('category_name')
        if not category_name:
            raise serializers.ValidationError('No name of the category was given')

        category.category_name = validated_data['category_name']
        category.save()
        return category
