import hashlib
import hmac
import json

import pytest
from django.core.exceptions import PermissionDenied
from django.test.client import RequestFactory
from django.utils.six import BytesIO, text_type

from django_phaxio.signals import phaxio_callback
from django_phaxio.views import DIRECTION, PhaxioCallbackView
from tests.testapp import settings

try:
    # Django 1.10+
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


def create_valid_signature(url, parameters, files):
    token = settings.PHAXIO_CALLBACK_TOKEN
    url = "{}{}".format('http://testserver', url)

    # sort the post fields and add them to the URL
    for key in sorted(parameters.keys()):
        url += '{}{}'.format(key, parameters[key])

    # sort the files and add their SHA1 sums to the URL
    for filename in sorted(files.keys()):
        file_hash = hashlib.sha1()
        file_hash.update(files[filename].read())
        url += '{}{}'.format(filename, file_hash.hexdigest())
    return hmac.new(
        key=token.encode('utf-8'),
        msg=url.encode('utf-8'),
        digestmod=hashlib.sha1
    ).hexdigest()


fax_data = {
    "id": 12444660,
    "num_pages": 1,
    "cost": 7,
    "direction": "received",
    "status": "success",
    "is_test": False,
    "requested_at": 1433914489,
    "completed_at": 1433914488,
    "from_number": "+16504888494",
    "to_number": "+13142666714",
}


@pytest.yield_fixture()
def valid_request():
    rf = RequestFactory()
    url = reverse('phaxio:callback')

    data = {
        'direction': DIRECTION.received,
        'fax': json.dumps(fax_data),
        'is_test': False,
        'metadata': 'some data',
    }
    with BytesIO() as f:
        f.write(b'some content')
        files = {'fax_01.pdf': f}
        valid_signature = create_valid_signature(url, data, files.copy())
        rf.defaults['HTTP_X_PHAXIO_SIGNATURE'] = valid_signature
        request = rf.post(url, data)
        request.FILES.update(files)
        yield request


class TestPhaxioCallbackView(object):
    def test_valid_signature(self, valid_request):
        response = PhaxioCallbackView.as_view()(valid_request)
        assert response.status_code == 200

    def test_invalid_signature(self, valid_request, caplog):
        # Django's QueryDict is immutable, so make a copy first
        valid_request.POST = valid_request.POST.copy()

        valid_request.POST['is_test'] = 'true'
        with pytest.raises(PermissionDenied):
            PhaxioCallbackView.as_view()(valid_request)

        msg = "Request signature did not match."
        assert msg in caplog.text()

    def test_signal(self, valid_request):
        class TestException(Exception):
            pass

        def signal_receiver(sender, **kwargs):
            raise TestException('signal received')

        phaxio_callback.connect(signal_receiver)

        with pytest.raises(TestException) as e:
            PhaxioCallbackView.as_view()(valid_request)
        phaxio_callback.disconnect(signal_receiver)
        assert text_type(e).endswith('signal received')

    def test_signal_kwargs(self, valid_request):
        def signal_receiver(
                sender, direction, fax, is_test, metadata, **kwargs):
            assert direction == DIRECTION.received
            assert not is_test
            assert fax == fax_data
            assert metadata == 'some data'

        phaxio_callback.connect(signal_receiver)
        PhaxioCallbackView.as_view()(valid_request)
        phaxio_callback.disconnect(signal_receiver)

    def test_no_signature(self, caplog):
        rf = RequestFactory()
        url = reverse('phaxio:callback')

        data = {
            'direction': DIRECTION.received,
            'fax': json.dumps(fax_data),
            'is_test': False,
            'metadata': 'some data',
        }
        request = rf.post(url, data)
        with pytest.raises(PermissionDenied):
            PhaxioCallbackView.as_view()(request)
        msg = ("The request header did not include a signature "
               "(X-Phaxio-Signature).")
        assert msg in caplog.text()
