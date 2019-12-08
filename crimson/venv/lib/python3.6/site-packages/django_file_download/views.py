# -*- coding: utf-8 -*-

from __future__ import division

import hashlib

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django_logit import logit
from django_response import response
from TimeConvert import TimeConvert as tc


def djfile_content_storage(content, ext='jpeg', base_path='file', file_path=None):
    if not file_path:
        # Joint File Path
        # Base Path
        base_path = settings.DJANGO_FILE_DOWNLOAD_BASE_PATH if hasattr(settings, 'DJANGO_FILE_DOWNLOAD_BASE_PATH') else base_path
        # YM Path
        ym_path = tc.local_string(format='%Y%m') if hasattr(settings, 'DJANGO_FILE_DOWNLOAD_USE_YM') and settings.DJANGO_FILE_DOWNLOAD_USE_YM else ''
        # File Name
        file_name = tc.local_string(format='%Y%m%d%H%M%S') if hasattr(settings, 'DJANGO_FILE_DOWNLOAD_USE_DT') and settings.DJANGO_FILE_DOWNLOAD_USE_DT else hashlib.md5(content).hexdigest()
        # File Path
        file_path = '{0}/{1}{2}{3}.{4}'.format(base_path, ym_path, ym_path and '/', file_name, ext)

    # File Save
    if not default_storage.exists(file_path):
        default_storage.save(file_path, ContentFile(content))

    # File URL
    file_url = '{0}{1}'.format(settings.DOMAIN if hasattr(settings, 'DOMAIN') else '', default_storage.url(file_path))

    return file_path, file_url


def djfile_res_storage(res, ext='jpeg', base_path='file', file_path=None):
    # File Ext
    ext = res.headers.get('Content-Type', '').split('/')[-1] or ext

    return djfile_content_storage(res.content, ext=ext, base_path=base_path, file_path=file_path)


def djfile_download(url):
    res = requests.get(url, verify=False)

    return djfile_res_storage(res)


@logit
def file_download(request):
    url = request.POST.get('url', '')

    # URL Not Found
    if not url:
        return response(settings.DJANGO_FILE_DOWNLOAD_URL_NOT_FOUND if hasattr(settings, 'DJANGO_FILE_DOWNLOAD_URL_NOT_FOUND') else 999998)

    file_path, file_url = djfile_download(url)

    if hasattr(settings, 'DJANGO_FILE_DOWNLOAD_CALLBACK_FUNC') and hasattr(settings.DJANGO_FILE_DOWNLOAD_CALLBACK_FUNC, '__call__'):
        settings.DJANGO_FILE_DOWNLOAD_CALLBACK_FUNC(request, file_path, file_url)

    return response(200, 'File Download Success', u'文件下载成功', data={
        'file_path': file_path,
        'file_url': file_url,
    })
