from rest_framework import serializers

from .models import Order, OrderDetail, Product


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=False)

    class Meta:
        model = Product
        fields = ('id', 'name')


class OrderDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    product = ProductSerializer()

    class Meta:
        model = OrderDetail
        fields = ('id', 'product', 'amount', 'price',)


class OrderSerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True)
    created_at = serializers.DateTimeField(
        format='%d-%m-%Y %H:%M:%S',
        read_only=True
    )

    class Meta:
        model = Order
        fields = ('id', 'status', 'created_at', 'external_id', 'details')
        read_only_fields = ('id', 'status')

    def create(self, validated_data):
        details = validated_data.pop('details')
        order = Order.objects.create(**validated_data)
        for detail in details:
            product_data = detail.pop('product')
            product, created = Product.objects.get_or_create(**product_data)
            OrderDetail.objects.create(**detail, order=order, product=product)
        return order

    def update(self, instance, validated_data):
        pass
