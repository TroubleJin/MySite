from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.views import Response
from rest_framework import status

def exception_handler(exc,context):
    response = drf_exception_handler(exc,context)
    print(exc)
    print(context)
    if response is None:
        return Response({
            'detail': '服务器错误'
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return response