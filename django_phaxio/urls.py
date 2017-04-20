from django.conf.urls import url

from . import views

# Set application namespace (Django 2.0+)
# https://docs.djangoproject.com/en/dev/topics/http/urls/#url-namespaces-and-included-urlconfs
app_name = 'django_phaxio'

urlpatterns = [
    url(r'^callback$',
        views.PhaxioCallbackView.as_view(),
        name='callback'),
]
