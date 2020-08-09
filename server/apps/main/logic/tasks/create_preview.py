import os

from django.conf import settings
from django.core.files.base import ContentFile
from preview_generator.manager import PreviewManager

from server.apps.main.models import VideoResource, Status
from server.settings.components.celery import app


@app.task(autoretry_for=(Exception,))
def create_preview(video_resource_id: int) -> int:
    """Task creates preview (thumbnails) for video

    Args:
        video_resource_id: ID of VideoResource instance

    Returns:
        ID of VideoResource instance

    """
    video_resource_instance = VideoResource.objects.get(pk=video_resource_id)
    video_resource_instance.status = Status.PREVIEW_CREATION
    video_resource_instance.save()

    manager = PreviewManager(settings.PREVIEW_ROOT, create_folder=True)
    video = video_resource_instance.videos.filter(primary=True).first()
    path_to_preview_image = manager.get_jpeg_preview(
        video.video.path,
        width=640,
        height=360,
    )
    name = path_to_preview_image.split('/')[-1]
    os.rename(
        path_to_preview_image, settings.PREVIEW_ROOT.joinpath(name),
    )
    os.remove(settings.PREVIEW_ROOT.joinpath(name.split('-')[0] + '.lock'))

    video_resource_instance.preview.save(
        name, ContentFile(open(settings.PREVIEW_ROOT.joinpath(name), 'rb').read()),
    )

    return video_resource_instance.id
