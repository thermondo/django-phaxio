from django.urls import include, path

urlpatterns = [
    path('phaxio/', include('django_phaxio.urls', namespace='phaxio')),
]
