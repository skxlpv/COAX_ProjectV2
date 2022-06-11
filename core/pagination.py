from rest_framework.pagination import PageNumberPagination


class LargeResults(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResults(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class SmallResults(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 20