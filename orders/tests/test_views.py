import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from orders.models import Order, OrderDetail, Product, Status
from orders.serializers import OrderSerializer


ACCEPT_URL = reverse('orders-accept', kwargs={'pk': 1})
DETAIL_URL = reverse('orders-detail', kwargs={'pk': 1})
FAIL_URL = reverse('orders-fail', kwargs={'pk': 1})
LIST_URL = reverse('orders-list')


class ViewsTest(APITestCase):

    def setUp(self):
        super().setUp()
        self.product = Product.objects.create(name='Test_product')
        self.order = Order.objects.create(external_id='test_ext_id')
        self.order_detail = OrderDetail.objects.create(
            product=self.product,
            order=self.order,
            amount=5,
            price=7.95
        )

    def test_user_can_get_all_orders(self):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        response = self.client.get(LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_user_can_get_order_retrieve(self):
        order = self.order
        serializer = OrderSerializer(order)
        response = self.client.get(DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_order_with_status_new_update_only_external_id_field(self):
        order = self.order
        serializer = OrderSerializer(order)
        new_details = {
            'product': {'id': 2, 'name': 'new_test_product'},
            'price': 100,
            'amount': 100.00,
            'order': 1
        }
        put_data = {
            'id': 2,
            'status': Status.ACCEPTED,
            'external_id': 'wrong_test_id',
            'details': new_details
        }
        response = self.client.put(DETAIL_URL, put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], serializer.data['id'])
        self.assertEqual(response.data['details'], serializer.data['details'])
        self.assertEqual(response.data['status'], serializer.data['status'])
        self.assertEqual(response.data['created_at'],
                         serializer.data['created_at'])
        self.assertNotEqual(response.data['external_id'],
                            serializer.data['external_id'])  # it is changed, whereas others no.
        self.assertEqual(response.data['external_id'], 'wrong_test_id')

    def test_order_with_status_failed_does_not_updated(self):
        fail_res = self.client.post(FAIL_URL)
        self.assertEqual(fail_res.data['status'], Status.FAILED)
        new_details = {
            'product': {'id': 2, 'name': 'new_test_product'},
            'price': 100,
            'amount': 100.00,
            'order': 1
        }
        put_data = {
            'id': 2,
            'status': Status.ACCEPTED,
            'external_id': 'wrong_test_id',
            'details': new_details
        }
        put_resp = self.client.put(DETAIL_URL, put_data, format='json')
        self.assertEqual(put_resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_order_with_status_accepted_does_not_updated(self):
        accept_res = self.client.post(ACCEPT_URL)
        self.assertEqual(accept_res.data['status'], Status.ACCEPTED)
        new_details = {
            'product': {'id': 2, 'name': 'new_test_product'},
            'price': 100,
            'amount': 100.00,
            'order': 1
        }
        put_data = {
            'id': 2,
            'status': Status.FAILED,
            'external_id': 'wrong_test_id',
            'details': new_details
        }
        put_resp = self.client.put(DETAIL_URL, put_data, format='json')
        self.assertEqual(put_resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_order_status_changes_to_accepted(self):
        accept_res = self.client.post(ACCEPT_URL)
        self.assertEqual(accept_res.status_code, status.HTTP_200_OK)
        self.assertEqual(accept_res.data['status'], Status.ACCEPTED)

    def test_order_status_changes_to_failed(self):
        response = self.client.post(FAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], Status.FAILED)

    def test_order_with_status_accepted_could_not_be_deleted(self):
        response = self.client.post(ACCEPT_URL)
        self.assertEqual(response.data['status'], Status.ACCEPTED)
        remove_res = self.client.delete(DETAIL_URL)
        self.assertEqual(remove_res.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_order_with_status_failed_could_be_deleted(self):
        response = self.client.post(FAIL_URL)
        self.assertEqual(response.data['status'], Status.FAILED)
        remove_res = self.client.delete(DETAIL_URL)
        self.assertEqual(remove_res.status_code, status.HTTP_204_NO_CONTENT)

    def test_order_with_status_new_could_be_deleted(self):
        order = self.order
        serializer = OrderSerializer(order)
        response = self.client.get(DETAIL_URL)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        remove_res = self.client.delete(DETAIL_URL)
        self.assertEqual(remove_res.status_code, status.HTTP_204_NO_CONTENT)

    def test_new_order_created_with_status_new(self):
        order = self.order
        statuses = ['', Status.ACCEPTED, Status.FAILED]
        for order_status in statuses:
            order.status = order_status
            serializer = OrderSerializer(order)
            response = self.client.post(
                LIST_URL,
                data=json.dumps(serializer.data),
                content_type='application/json'
            )
            self.assertEqual(response.data['status'], Status.NEW)

