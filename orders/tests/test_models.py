from rest_framework.test import APITestCase

from orders.models import Order, OrderDetail, Product, Status


class ModelsTest(APITestCase):
    @classmethod
    def setUp(cls):
        super().setUpClass()
        cls.product = Product.objects.create(name='Test_product')
        cls.order = Order.objects.create(external_id='test_ext_id')
        cls.order_detail = OrderDetail.objects.create(
            product=cls.product,
            order=cls.order,
            amount=5,
            price=7.55
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_order_created_with_status_new(self):
        order = ModelsTest.order
        self.assertEqual(Status.NEW, order.status)

    def test_order_model_verbose_names(self):
        order = ModelsTest.order
        field_verboses = {
            'status': 'Status',
            'created_at': 'Creation date',
            'external_id': 'External identifier'
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    order._meta.get_field(value).verbose_name, expected)

    def test_product_model_verbose_names(self):
        product = ModelsTest.product
        field_verbose = {'name': "Product"}
        self.assertEqual(product._meta.get_field('name').verbose_name,
                         field_verbose['name'])

    def test_order_detail_model_verbose_names(self):
        order_detail = ModelsTest.order_detail
        field_verboses = {
            'amount': 'Amount',
            'price': 'Price'
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    order_detail._meta.get_field(value).verbose_name, expected)

    def test_product_appears_as_name_field(self):
        self.assertEqual(ModelsTest.product.name, str(ModelsTest.product))
