from django.urls import path, include
from rest_framework.routers import DefaultRouter

from server.apps.main.api.v1.views import video_resource as video_resource_views

app_name = 'main_v1'

router = DefaultRouter()
router.register(r'videos', video_resource_views.VideoResourceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
