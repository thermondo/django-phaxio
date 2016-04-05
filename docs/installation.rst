Installation
============

Simply install the latest stable package using the command

``pip install django-phaxio``

add ``'django_phaxio'`` to the ``INSTALLED_APP`` setting in your ``settings.py``

and add

``url(r'^phaxio/', include('django_phaxio.urls', namespace='phaxio')),``

to your ``urlpatterns`` in your URL root configuration.

.. automodule:: django_phaxio.conf
    :members:
    :undoc-members:
    :show-inheritance:
