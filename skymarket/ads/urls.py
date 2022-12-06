from django.urls import include, path
from rest_framework import routers

from ads.views import AdViewSet

ads_router = routers.SimpleRouter()
ads_router.register('', AdViewSet)

urlpatterns = [
    path("", include(ads_router.urls)),
]
