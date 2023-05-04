from rest_framework.pagination import PageNumberPagination


class PagePaginations(PageNumberPagination):
    page_size = 5
