from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Status, Order, Product
from .serializers import OrderSerializer, OrderUpdateOnlySerializer


NOT_NEW_ORDER_STATUS_TEXT = 'Only orders with status "new" could be changed.'
NO_PRODUCT_FOUND_TEXT = 'No product with such id in database.'


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filterset_fields = ['external_id', 'status', ]

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Changes status of order to 'accepted'."""
        order = get_object_or_404(Order, pk=pk)
        order.status = Status.ACCEPTED
        order.save()
        serializer = self.get_serializer(order)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def fail(self, request, pk=None):
        """Changes status of order to 'failed'."""
        order = get_object_or_404(Order, pk=pk)
        order.status = Status.FAILED
        order.save()
        serializer = self.get_serializer(order)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_details = serializer.validated_data.get('details')
        try:
            product_data = order_details[0]
        except IndexError:
            no_details_text = 'Order details should pointed.'
            return Response(no_details_text,
                            status=status.HTTP_400_BAD_REQUEST)
        user_given_product = product_data.get('product')
        user_product_id = user_given_product.get('id')
        if not Product.objects.filter(id=user_product_id).exists():
            return Response(
                NO_PRODUCT_FOUND_TEXT,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        if order.status != Status.NEW:
            return Response(NOT_NEW_ORDER_STATUS_TEXT,
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        order.external_id = self.kwargs.get('external_id', order.external_id)
        serializer = OrderUpdateOnlySerializer(
            instance=order,
            data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        if order.status == Status.ACCEPTED:
            return Response(
                f'Order with status {Status.ACCEPTED} could not be deleted.',
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
