from urllib.request import urlretrieve

from django.core.files.base import ContentFile

from server.apps.main.models import VideoResource, Video
from server.settings.components.celery import app


@app.task(autoretry_for=(Exception,))
def download_video(url: str, video_resource_id: int) -> int:
    """Task creates preview (thumbnails) for video

    Args:
        url: ID of VideoResource instance
        video_resource_id: ID of VideoResource instance


    Return:
        ID of VideoResource instance

    """
    name = url.split('/')[-1]
    path, response = urlretrieve(url)
    video_resource_instance = VideoResource.objects.get(pk=video_resource_id)
    video = Video.objects.create(
        primary=True,
        video_resource=video_resource_instance,
        extension=name.split('.')[-1],
    )
    video.video.save(name, ContentFile(open(path, 'rb').read()))
    return video_resource_instance.id
