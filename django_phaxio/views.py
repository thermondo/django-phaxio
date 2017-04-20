import hashlib
import hmac
import json
import logging

from django.core.exceptions import PermissionDenied
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from .conf import settings
from .signals import phaxio_callback

logger = logging.getLogger('django-phaxio')


class DIRECTION:
    """
    Direction of a FAX object.

    A FAX can be ether ``sent`` or ``received``.
    """

    sent = 'sent'
    received = 'received'


DIRECTION_MAP = {
    'sent': DIRECTION.sent,
    'received': DIRECTION.received,
}


class PhaxioCallbackView(View):
    """A view to receive WebHooks from Phaxio."""

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """Disable CSRF but enable token based security."""
        self.validate_signature(request)
        return super(PhaxioCallbackView, self).dispatch(
            request, *args, **kwargs)

    def post(self, request):
        """Process WebHook and send :func:`.phaxio_callback` signal."""
        fax = request.POST["fax"]
        direction = request.POST['direction']
        is_test = request.POST['is_test']
        is_test = is_test in [1, '1', True, 'true', 'True']
        phaxio_callback.send(
            sender=PhaxioCallbackView,
            direction=DIRECTION_MAP[direction],
            fax=json.loads(fax),
            metadata=request.POST.get('metadata', ''),
            is_test=is_test,
        )
        return JsonResponse({})

    @staticmethod
    def validate_signature(request):
        """
        Create signature for payload and compare provided signature.

        The signature is stored in the header ``X-Phaxio-Signature``.

        Raises:
            PermissionDenied: If provided signature and calculated
            signature do not match.

        """
        try:
            signature = request.META['HTTP_X_PHAXIO_SIGNATURE']
        except KeyError:
            logger.warning(
                'The request header did not include '
                'a signature (X-Phaxio-Signature).')
            raise PermissionDenied

        token = settings.PHAXIO_CALLBACK_TOKEN
        url = request.build_absolute_uri()
        parameters = request.POST.copy()
        files = request.FILES.copy()

        # sort the post fields and add them to the URL
        for key in sorted(parameters.keys()):
            url += '{}{}'.format(key, parameters[key])

        # sort the files and add their SHA1 sums to the URL
        for filename in sorted(files.keys()):
            file_hash = hashlib.sha1()
            file_hash.update(files[filename].read())
            url += '{}{}'.format(filename, file_hash.hexdigest())
        expected_signature = hmac.new(
            key=token.encode('utf-8'), msg=url.encode('utf-8'),
            digestmod=hashlib.sha1).hexdigest()
        if signature != expected_signature:
            logger.warning(
                "Request signature did not match.\n"
                "Expected signature: %s\n"
                "Received signature: %s\n",
                expected_signature, signature)
            raise PermissionDenied
