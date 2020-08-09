from server.apps.main.models import VideoResource, Status
from server.settings.components.celery import app


@app.task(autoretry_for=(Exception,))
def update_video_resource_status(video_resource_id: int, status: Status) -> int:
    """Task updates VideoResource status.

    Args:
        video_resource_id: ID of VideoResource instance
        status: New VideoResource status

    Returns:
        ID of VideoResource instance

    """
    video_resource_instance = VideoResource.objects.get(pk=video_resource_id)
    video_resource_instance.status = status
    video_resource_instance.save()
    return video_resource_instance.pk
