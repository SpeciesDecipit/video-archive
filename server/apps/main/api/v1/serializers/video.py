from rest_framework.serializers import ModelSerializer

from server.apps.main.models import Video


class BaseVideoSerializer(ModelSerializer):
    """Base serializer for Video model"""

    class Meta(object):
        model = Video
        fields = ('video', 'extension', 'primary')


class GetVideoSerializer(BaseVideoSerializer):
    """Base serializer for Video model."""
