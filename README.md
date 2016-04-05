[![Django-CC](https://img.shields.io/badge/Django-CC-ee66dd.svg)](https://github.com/codingjoe/django-cc)
[![version](https://img.shields.io/pypi/v/django-phaxio.svg)](https://pypi.python.org/pypi/django-phaxio/)
[![ci](https://api.travis-ci.org/Thermondo/django-phaxio.svg?branch=master)](https://travis-ci.org/Thermondo/django-phaxio)
[![coverage](https://coveralls.io/repos/Thermondo/django-phaxio/badge.svg?branch=master)](https://coveralls.io/r/Thermondo/django-phaxio)
[![code-health](https://landscape.io/github/Thermondo/django-phaxio/master/landscape.svg?style=flat)](https://landscape.io/github/Thermondo/django-phaxio/master)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/Thermondo/django-phaxio?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

# Django Phaxio
Django WebHooks for [Phaxio] callbacks.

## Installation

Simply install the latest stable package using the command

```shell
pip install django-phaxio
```

add `'django_phaxio',` to `INSTALLED_APP`s in your settings.py

and add

```python
url(r'^phaxio/', include('django_phaxio.urls', namespace='phaxio')),
```

to your ``urlpatterns`` in your URL root configuration.

You will also need to set the [Phaxio] callback token for security.

`PHAXIO_CALLBACK_TOKEN` (required):

Callback token provided by Phaxio to verify the request origin.

See https://www.phaxio.com/docs/security/callbacks

## Documentation
The latest documentation can be found at [Read the Docs](http://django-phaxio.rtfd.org/).

## Contribution
Please read the [Contributing Guide](CONTRIBUTING.md) before you submit a pull request.

[Phaxio]: https://www.phaxio.com
