from django.urls import include, path
from rest_framework import routers

from ads.views import AdViewSet, AdsByUserListView

ads_router = routers.SimpleRouter()
ads_router.register('', AdViewSet)

urlpatterns = [
    path('me/', AdsByUserListView.as_view()),
    path("", include(ads_router.urls)),
]
