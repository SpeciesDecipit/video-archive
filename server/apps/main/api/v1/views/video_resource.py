from typing import Dict, Type

from rest_framework.serializers import ModelSerializer

from server.apps.main.api.base.view import SerializerMappingModelViewSet
from server.apps.main.api.v1.serializers.video_resource import (
    BaseVideoResourceSerializer,
    PostVideoResourceSerializer,
)
from server.apps.main.models import VideoResource


class VideoResourceViewSet(SerializerMappingModelViewSet):
    """The view provides List/Detail access to VideoResource resource."""

    http_method_names = ('get', 'post')
    queryset = VideoResource.objects.all()
    serializers_mapping: Dict[str, Type[ModelSerializer]] = {
        'GET': BaseVideoResourceSerializer,
        'POST': PostVideoResourceSerializer,
    }
