# -*- coding: utf-8 -*-

from django.conf.urls import url
from django_file_download import views as file_views


app_name = 'django_file_download'


urlpatterns = [
    url(r'^download$', file_views.file_download, name='file_download'),
]
