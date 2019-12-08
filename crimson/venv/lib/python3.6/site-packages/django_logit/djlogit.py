# -*- coding: utf-8 -*-

import logging
from functools import wraps

from django.conf import settings


logger = logging.getLogger('logit')


def loggerit(func, flag, content):
    logger.debug('func=%s&flag=%s&content=%s', func, flag, content)


def logit(func=None, body=False, res=False, session=False, cookie=False):
    def decorator(func):
        @wraps(func)
        def with_logging(request, *args, **kwargs):
            # Get Func Name
            name = func.__name__

            if hasattr(settings, 'DJANGO_LOGIT_ENABLED') and settings.DJANGO_LOGIT_ENABLED:

                # Body Content Section
                if body:
                    try:
                        loggerit(name, 'body', request.body)
                    except Exception as e:
                        loggerit(name, 'error', e.message)

                # Get Content Section
                rgets = request.GET
                if rgets:
                    loggerit(name, 'get', request.GET)

                # POST Content Section
                rposts = request.POST
                if rposts:
                    loggerit(name, 'post', request.POST)

                # Session Content Section
                if session:
                    session_items = request.session.items()
                    if session_items:
                        loggerit(name, 'session', session_items)

                # Cookie Content Section
                if cookie:
                    cookies = request.COOKIES
                    if cookies:
                        loggerit(name, 'cookie', cookies)

                response = func(request, *args, **kwargs)

                # Response Content Section
                if res:
                    try:
                        loggerit(name, 'res', response.content)
                    except Exception as e:
                        loggerit(name, 'error', e.message)

                return response

            return func(request, *args, **kwargs)

        return with_logging

    if not func:
        def decorator2(func):
            return decorator(func)

        return decorator2

    return decorator(func)
