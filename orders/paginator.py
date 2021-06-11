from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


def calc_end_index(items_qty: int, limit_value: int, start_index: int) -> int:
    """
    Calculate index of last item that could be taken into account. It should
    not exceed index of the last item in whole array.
    :param items_qty: total amount of items in whole array.
    :param limit_value: max level of items could be taken into account.
    :param start_index: index of the first item will be taken into account.
    :return: index of the last item taken into account.
    """
    if limit_value >= items_qty:
        return items_qty - 1  # need minus one because we are looking for index, which starts from zero.
    else:
        last_index = start_index + limit_value - 1
        return min(last_index, items_qty - 1)


class CustomPagination(LimitOffsetPagination):

    def get_paginated_response(self, data):
        total_items = self.count
        items_start_idx = self.offset
        if items_start_idx >= total_items:
            headers = {'Content-Range': f'-/{total_items}'}
            return Response(data, headers=headers)

        try:
            items_end_idx = calc_end_index(
                total_items, self.limit, items_start_idx
            )
        except ValueError:
            pass
        headers = {
            'Content-Range': f'{items_start_idx}-{items_end_idx}/{total_items}'
        }
        return Response(data, headers=headers)
