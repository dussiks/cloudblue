from rest_framework import serializers

from .models import Order, OrderDetail, Product


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=False)

    class Meta:
        model = Product
        fields = ('id', 'name')


class OrderDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    product = ProductSerializer()

    class Meta:
        model = OrderDetail
        fields = ('id', 'product', 'amount', 'price')


class OrderUpdateOnlySerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ('id', 'status', 'created_at', 'external_id', 'details')
        read_only_fields = ('id', 'status', 'created_at', 'details')

    def to_internal_value(self, data):
        in_data = {}
        for key, value in data.items():
            if key == 'external_id':
                in_data[key] = value
        return in_data


class OrderSerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True)  # this is variant as details should be in each order.

    class Meta:
        model = Order
        fields = ('id', 'status', 'created_at', 'external_id', 'details')
        read_only_fields = ('id', 'status', 'created_at')

    def create(self, validated_data):
        details = validated_data.pop('details')
        order = Order.objects.create(**validated_data)
        for detail in details:
            product_data = detail.pop('product')
            product, created = Product.objects.get_or_create(**product_data)
            OrderDetail.objects.create(**detail, order=order, product=product)  # I set that just created products could be choosen.
        return order
