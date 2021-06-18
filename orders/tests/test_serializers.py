from rest_framework.test import APITestCase

from orders.models import Order, OrderDetail, Product, Status
from orders.serializers import (OrderSerializer, OrderDetailSerializer,
                                OrderUpdateOnlySerializer, ProductSerializer)


class ProductSerializerTest(APITestCase):

    def setUp(self):
        super().setUp()
        self.product_attributes = {
            'id': 1,
            'name': 'test_product',
        }
        self.product = Product.objects.create(**self.product_attributes)
        self.serializer = ProductSerializer(instance=self.product)

    def test_product_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['name', 'id'])

    def test_product_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.product_attributes['name'])


class OrderDetailsSerializerTest(APITestCase):

    def setUp(self):
        super().setUp()
        self.product = Product.objects.create(name='test_product')
        self.order = Order.objects.create(external_id='test_external_id')
        self.order_detail_attributes = {
            'id': 1,
            'amount': 10,
            'price': 15.78,
            'order': self.order,
            'product': self.product
        }
        self.order_detail = OrderDetail.objects.create(
            **self.order_detail_attributes
        )
        self.serializer = OrderDetailSerializer(instance=self.order_detail)

    def test_order_details_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(),
                              ['id', 'price', 'product', 'amount'])

    def test_order_details_fields_content(self):
        data = self.serializer.data
        self.assertEqual(data['amount'],
                         self.order_detail_attributes['amount'])
        self.assertEqual(data['id'], self.order_detail_attributes['id'])
        self.assertEqual(data['price'],
                         str(self.order_detail_attributes['price']))


class OrderSerializerTest(APITestCase):

    def setUp(self):
        super().setUp()
        self.product = Product.objects.create(name='test_product')
        self.order_attributes = {
            'id': 1,
            'status': Status.NEW,
            'external_id': 'some_test_external_id'
        }
        self.order = Order.objects.create(**self.order_attributes)
        self.order_detail = OrderDetail.objects.create(
            id=1,
            amount=10,
            price=19.77,
            order=self.order,
            product=self.product
        )

        self.serializer = OrderSerializer(instance=self.order)

    def test_order_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            ['id', 'status', 'external_id', 'details', 'created_at']
        )

    def test_order_fields_content(self):
        data = self.serializer.data
        self.assertEqual(data['id'], self.order_attributes['id'])
        self.assertEqual(data['status'], self.order_attributes['status'])
        self.assertEqual(data['external_id'],
                         self.order_attributes['external_id'])

    def test_order_serialization_fails_without_details(self):
        """Verify order_details field required for order serialization."""
        wrong_data = {
            'id': 3,
            'status': Status.NEW,
            'external_id': 'some_test_external_id'
        }
        wrong_serializer = OrderSerializer(data=wrong_data)
        self.assertFalse(wrong_serializer.is_valid())

        true_data = {
            'id': 3,
            'status': Status.NEW,
            'external_id': 'some_test_external_id',
            'details': [OrderDetailSerializer(self.order_detail).data]
        }
        true_serializer = OrderSerializer(data=true_data)
        self.assertTrue(true_serializer.is_valid())


class OrderUpdateOnlySerializerTest(APITestCase):

    def setUp(self):
        super().setUp()
        self.product = Product.objects.create(name='test_product')
        self.order_attributes = {
            'id': 1,
            'status': Status.NEW,
            'external_id': 'some_test_external_id'
        }
        self.order = Order.objects.create(**self.order_attributes)
        self.order_detail = OrderDetail.objects.create(
            id=1,
            amount=10,
            price=19.77,
            order=self.order,
            product=self.product
        )

        self.serializer = OrderUpdateOnlySerializer(instance=self.order)

    def test_order_update_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            ['id', 'status', 'external_id', 'details', 'created_at']
        )

    def test_order_update_serialization_takes_only_external_id(self):
        """Verify if only external_id field is taken for deserialization."""
        enough_data = {
            'external_id': 'some_test_external_id'
        }
        serializer = OrderUpdateOnlySerializer(data=enough_data)
        self.assertTrue(serializer.is_valid())
