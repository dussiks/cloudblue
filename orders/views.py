from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Status, Order, OrderDetail, Product
from .serializers import (
    OrderSerializer, OrderDetailSerializer, ProductSerializer
)


NOT_NEW_ORDER_STATUS_TEXT = 'Only "new" status of order could be changed.'


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filterset_fields = ['external_id', 'status', ]

    @action(detail=True, methods=['post'], url_path='accept')
    def change_status_to_accepted(self, request, pk=None):
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

    def destroy(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        if order.status == Status.ACCEPTED:
            return Response(
                f'Order with status "accepted" could not be deleted.',
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        self.perform_destroy(order)
        return Response(status=status.HTTP_204_NO_CONTENT)

