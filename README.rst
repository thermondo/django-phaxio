|version| |ci| |coverage| |license|

Django Phaxio
=============

Django WebHooks for `Phaxio`_ callbacks.

Installation
------------

Simply install the latest stable package using the command

.. code:: shell

    pip install django-phaxio

add ``'django_phaxio',`` to ``INSTALLED_APP``\ s in your settings.py

and add

.. code:: python

    path('phaxio/', include('django_phaxio.urls', namespace='phaxio')),

to your ``urlpatterns`` in your URL root configuration.

You will also need to set the `Phaxio`_ callback token for security.

``PHAXIO_CALLBACK_TOKEN`` (required):

Callback token provided by Phaxio to verify the request origin.

See https://www.phaxio.com/docs/security/callbacks

Documentation
-------------

The latest documentation can be found at `Read the Docs`_.

Contribution
------------

Please read the `Contributing Guide`_ before you submit a pull request.

.. _Phaxio: https://www.phaxio.com
.. _Read the Docs: http://django-phaxio.rtfd.org/
.. _Contributing Guide: CONTRIBUTING.md

.. |version| image:: https://img.shields.io/pypi/v/django-phaxio.svg
   :target: https://pypi.python.org/pypi/django-phaxio/
.. |ci| image:: https://github.com/Thermondo/django-phaxio/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/Thermondo/django-phaxio/actions/workflows/ci.yml
.. |coverage| image:: https://codecov.io/gh/Thermondo/django-phaxio/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Thermondo/django-phaxio
.. |license| image:: https://img.shields.io/badge/license-APL_2-blue.svg
   :target: LICENSE
