from rest_framework.response import Response

class ApiResponse(Response):
    def __init__(self,data_status=0,data_msg='ok',results=None,http_status=None,headers=None,exception=False,content_type=None,**kwargs):
        data = {
            "status": data_status,
            "msg": data_msg,
        }
        if results is not None:
            data["results"] = results

        if kwargs is not None:
            data.update(kwargs.items())
        super().__init__(data=data, status=http_status,
                         headers=headers,exception=exception, content_type=content_type)


"""
Response({
    "status": 0,
    "msg": "ok',
    "results": [],
    "token": ""
},status=http_status,headers=headers,exception=True|False)
"""