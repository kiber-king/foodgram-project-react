from rest_framework import pagination

from core.constants import default_limit, max_limit, max_page_size, page_size


class CustomPagination(pagination.PageNumberPagination):
    page_size = page_size
    page_query_param = 'page'
    page_size_query_param = 'limit'
    max_page_size = max_page_size


class CartPagination(pagination.LimitOffsetPagination):
    default_limit = default_limit
    page_query_param = 'page'
    page_size_query_param = 'limit'
    max_limit = max_limit
