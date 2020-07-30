from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.views import Response

def exception_handler(exc,context):
    response = drf_exception_handler(exc,context)
    print(exc)
    print(context)
    if response is None:
        return Response({
            'detail': '服务器错误'
            }
        )
    return response