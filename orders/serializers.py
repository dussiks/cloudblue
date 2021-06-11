from rest_framework import serializers

from .models import Order, OrderDetail, Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name',)


class OrderDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderDetail
        fields = ('id', 'product', 'amount', 'price',)


class OrderSerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True)
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')

    class Meta:
        model = Order
        fields = ('id', 'status', 'created_at', 'external_id', 'details')
