from rest_framework.response import Response


class APIResponse(Response):
    def __init__(self, myStatus=True, msg='', data=None, status=200, headers=None, content_type=None, **kwargs):
        dic = {'myStatus': myStatus, 'msg': msg}
        if data is not None:
            dic['data'] = data

        dic.update(kwargs)
        super().__init__(data=dic, status=status,
                         template_name=None, headers=headers,
                         exception=False, content_type=content_type)
