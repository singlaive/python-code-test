from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^ships/$', views.ships, name='index'),
    url(r'^listings/$', views.listings, name='listings'),
    url(r'^listings/(?P<list_id>[0-9]+)/$', views.listing_detail, name='activate_listing'),
]