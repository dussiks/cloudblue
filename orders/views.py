from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Status, Order, Product
from .serializers import OrderSerializer


NOT_NEW_ORDER_STATUS_TEXT = 'Only orders with status "new" could be changed.'
NO_PRODUCT_FOUND_TEXT = 'No product with such id in database.'


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filterset_fields = ['external_id', 'status', ]

    @action(detail=True, methods=['post'], url_path='accept')
    def change_status_to_accepted(self, request, pk=None):
        """
        Checks if the status of existing object is 'new' and changes it to
        'accepted'. Else, returns sufficient message to user and keeps status
        without changing.
        """
        order = get_object_or_404(Order, pk=pk)
        if order.status == Status.NEW:
            order.status = Status.ACCEPTED
            order.save()
            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            NOT_NEW_ORDER_STATUS_TEXT,
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=True, methods=['post'], url_path='fail')
    def change_status_to_failed(self, request, pk=None):
        """
        Checks if the status of existing object is 'new' and changes it to
        'failed'. Else, returns sufficient message to user and keeps status
        without changing.
        """
        order = get_object_or_404(Order, pk=pk)
        if order.status == Status.NEW:
            order.status = Status.FAILED
            order.save()
            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            NOT_NEW_ORDER_STATUS_TEXT,
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_details = serializer.validated_data.get('details')
        try:
            product_data = order_details[0]
        except IndexError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_given_product = product_data.get('product')
        user_product_id = user_given_product.get('id')
        if not Product.objects.filter(id=user_product_id).exists():
            return Response(
                NO_PRODUCT_FOUND_TEXT,
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)
        if order.status == Status.NEW:
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            NOT_NEW_ORDER_STATUS_TEXT,
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def destroy(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        if order.status == Status.ACCEPTED:
            return Response(
                f'Order with status {Status.ACCEPTED} could not be deleted.',
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        self.perform_destroy(order)
        return Response(status=status.HTTP_204_NO_CONTENT)
