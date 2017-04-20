"""
`Django signals`_ for Phaxio callbacks.

_`Django signals`: https://docs.djangoproject.com/en/stable/topics/signals/
"""
from django.dispatch import Signal

phaxio_callback = Signal(
    providing_args=[
        'direction',
        'fax',
        'metadata',
        'is_test',
    ]
)
"""
Signal that gets send for each Phaxio WebHook.

Args:
    direction (str): Either ``sent`` or ``received``.
    fax (dict): Fax object from JSON data.
    metadata (str): Meta data defined in job request.
    is_test (bool): Indicated whether or not it is a test call.


Example::

    from django.dispatch import receiver
    from django_phaxio.signals import phaxio_callback
    from django_phaxio.views import PhaxioCallbackView


    @receiver(phaxio_callback, sender=PhaxioCallbackView)
    def my_webhook_handler(
            sender, direction, fax, metadata, is_test, **kwargs):
        # Do something
        pass

"""
