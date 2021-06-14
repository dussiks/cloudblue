import datetime as dt

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
        read_only=True,
        default=serializers.CreateOnlyDefault(dt.datetime.now())
    )

    class Meta:
        model = Order
        fields = ('id', 'status', 'created_at', 'external_id', 'details')
        read_only_fields = ('id', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['view'].action == 'update':
            self.fields['details'].read_only = True

    def create(self, validated_data):
        details = validated_data.pop('details')
        order = Order.objects.create(**validated_data)
        for detail in details:
            product_data = detail.pop('product')
            product, created = Product.objects.get_or_create(**product_data)  # created just for serialization purpose.
            OrderDetail.objects.create(**detail, order=order, product=product)
        return order

    def update(self, instance, validated_data):
        instance.external_id = validated_data.get(
            'external_id', instance.external_id
        )
        instance.save()
        return instance
