from typing import List

from celery import chain

from server.apps.main.logic.tasks.create_preview import create_preview
from server.apps.main.logic.tasks.download_video import download_video
from server.apps.main.logic.tasks.recoding import recode_video
from server.apps.main.logic.tasks.video_resource_states import (
    update_video_resource_status,
)
from server.apps.main.models import Status
from server.settings.components.celery import app


@app.task(autoretry_for=(Exception,))
def pipeline_with_download_video(
    url: str, video_resource_id: int, target_formats: List[str],
) -> int:
    """Pipeline with downloading video.

    Args:
        url: ID of VideoResource instance
        video_resource_id: ID of VideoResource instance
        target_formats: List of target formats for video recoding

    Returns:
        ID of VideoResource instance

    """
    chain(
        download_video.s(url, video_resource_id),
        create_preview.s(),
        *[recode_video.s(target_format) for target_format in target_formats],
        update_video_resource_status.s(Status.READY),
    ).apply_async()
    return video_resource_id


@app.task(autoretry_for=(Exception,))
def pipeline_without_download_video(
    video_resource_id: int, target_formats: List[str],
) -> int:
    """Pipeline without downloading video.

    Args:
        video_resource_id: ID of VideoResource instance
        target_formats: List of target formats for video recoding

    Returns:
        ID of VideoResource instance

    """
    chain(
        create_preview.s(video_resource_id),
        *[recode_video.s(target_format) for target_format in target_formats],
        update_video_resource_status.s(Status.READY),
    ).apply_async()
    return video_resource_id
