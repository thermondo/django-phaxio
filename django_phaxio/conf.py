"""
Additional settings for Django.

``PHAXIO_CALLBACK_TOKEN`` (required):

    Callback token provided by Phaxio to verify the request origin.

    .. note:: See https://www.phaxio.com/docs/security/callbacks

"""
from appconf import AppConf
from django.conf import settings  # NoQA

__all__ = ('settings',)


class PhaxioConf(AppConf):
    class Meta:
        prefix = 'PHAXIO'
        required = ['CALLBACK_TOKEN']
