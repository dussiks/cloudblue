from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_query_param = 'offset'
    page_size_query_param = 'limit'
    page_size = 4

    def get_paginated_response(self, data):
        return Response(data)
