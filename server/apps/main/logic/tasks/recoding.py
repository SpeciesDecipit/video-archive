from typing import Dict, Any

from converter import Converter
from django.conf import settings
from django.core.files.base import ContentFile

from server.apps.main.models import VideoResource, Status, Video
from server.settings.components.celery import app


def get_options(meta, target_format: str) -> Dict[str, Any]:
    return {
        'mp4': {
            'format': 'mp4',
            'audio': {
                'codec': meta.audio.codec,
                'samplerate': meta.audio.bitrate,
                'channels': meta.audio.audio_channels,
            },
            'video': {
                'codec': meta.video.codec,
                'width': 640,
                'height': 360,
                'fps': int(meta.video.video_fps),
            },
            'subtitle': {'codec': 'copy'},
            'map': 0,
        },
        'webm': {
            'format': 'webm',
            'audio': {
                'codec': 'vorbis',
                'samplerate': meta.audio.bitrate,
                'channels': meta.audio.audio_channels,
            },
            'video': {
                'codec': 'vp8',
                'width': 640,
                'height': 360,
                'fps': int(meta.video.video_fps),
            },
            'subtitle': {'codec': 'copy'},
            'map': 0,
        },
    }[target_format]


@app.task(autoretry_for=(Exception,))
def recode_video(video_resource_id: int, target_format: str) -> int:
    """Method recode video to the particular format.

    Args:
        video_resource_id: ID of VideoResource instance
        target_format: Target format

    Returns:
        ID of VideoResource instance

    """
    video_resource_instance = VideoResource.objects.get(pk=video_resource_id)
    video_resource_instance.status = Status.RECODING
    video_resource_instance.save()

    if video_resource_instance.videos.filter(extension=target_format):
        return video_resource_instance.pk

    primary_video_instance = video_resource_instance.videos.filter(primary=True).first()
    name = primary_video_instance.video.path.split('/')[-1].split('.')[0]

    video_instance = Video.objects.create(
        video_resource=video_resource_instance, extension=target_format,
    )
    new_full_path = settings.VIDEO_ROOT.joinpath(f'{name}.{target_format}')

    converter = Converter()
    meta = converter.probe(str(primary_video_instance.video.path))
    conv = converter.convert(
        str(primary_video_instance.video.path),
        str(new_full_path),
        get_options(meta, target_format),
    )
    list(conv)

    video_instance.video.save(name, ContentFile(open(new_full_path, 'rb').read()))

    return video_resource_instance.id
