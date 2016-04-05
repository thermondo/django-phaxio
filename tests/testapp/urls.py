from django.conf.urls import include, url

urlpatterns = [
    url(r'^phaxio/', include('django_phaxio.urls', namespace='phaxio')),
]
