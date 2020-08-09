from typing import Dict, Any

from rest_framework.exceptions import ValidationError
from rest_framework.fields import FileField, URLField
from rest_framework.serializers import ModelSerializer

from server.apps.main.api.v1.serializers.video import GetVideoSerializer
from server.apps.main.logic.tasks.pipelines import (
    pipeline_with_download_video,
    pipeline_without_download_video,
)
from server.apps.main.models import VideoResource, Video


class BaseVideoResourceSerializer(ModelSerializer):
    """Base serializer for VideoResource model"""

    videos = GetVideoSerializer(many=True, read_only=True)

    class Meta(object):
        model = VideoResource
        fields = ('id', 'title', 'preview', 'status', 'videos')


class PostVideoResourceSerializer(BaseVideoResourceSerializer):
    """Post serializer for VideoResource model."""

    video = FileField(write_only=True, required=False)
    url = URLField(write_only=True, required=False)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        video = attrs.get('video')
        url = attrs.get('url')

        if not video and not url:
            raise ValidationError('Video or URL should be provided')

        return attrs

    def create(self, validated_data: Dict[str, Any]) -> VideoResource:
        url = validated_data.pop('url', None)
        video = validated_data.pop('video', None)
        video_resource = super().create(validated_data)

        if url:
            pipeline_with_download_video.apply_async(
                args=(url, video_resource.id, ['mp4', 'webm']),
            )
        elif video:
            Video.objects.create(
                video=video,
                extension=video.name.split('.')[-1],
                video_resource=video_resource,
                primary=True,
            )
            pipeline_without_download_video.apply_async(
                args=(video_resource.id, ['mp4', 'webm']),
            )
        return video_resource

    class Meta(BaseVideoResourceSerializer.Meta):
        fields = BaseVideoResourceSerializer.Meta.fields + ('video', 'url')
