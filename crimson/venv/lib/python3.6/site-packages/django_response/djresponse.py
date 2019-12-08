# -*- coding: utf-8 -*-

from json_response import JsonpResponse, JsonResponse
from StatusCode import StatusCodeField


def response_data(status_code=200, message=None, description=None, data={}, **kwargs):
    return dict({
        'status': status_code,
        'message': message,
        'description': description,
        'data': data,
    }, **kwargs)


def response(status_code=200, message=None, description=None, data={}, msg_args=[], msg_kwargs={}, desc_args=[], desc_kwargs={}, request=None, callback=None, **kwargs):
    # Final Message and Description
    message, description = (message or status_code.message, description or status_code.description) if isinstance(status_code, StatusCodeField) else (message, description)
    # Final Response Data
    resp_data = response_data(status_code, (message or '').format(*msg_args, **msg_kwargs), (description or '').format(*desc_args, **desc_kwargs), data, **kwargs)
    # Assign Callback
    callback = callback or (request and request.GET.get('callback'))
    # Call JsonResponse or JsonpResponse
    return JsonpResponse(callback, resp_data, safe=False) if callback else JsonResponse(resp_data, safe=False)
