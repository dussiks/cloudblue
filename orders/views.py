from rest_framework import status, viewsets
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
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
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
