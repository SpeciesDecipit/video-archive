import pytest

from server.apps.main.logic.tasks.create_preview import create_preview
from server.apps.main.models import VideoResource, Status


@pytest.mark.django_db
def test_create_preview(video_resource: VideoResource) -> None:
    """Test checks creation of preview for video"""
    create_preview(video_resource.id)
    video_resource.refresh_from_db()

    assert video_resource.preview
    assert video_resource.preview.open()
    assert video_resource.status == Status.PREVIEW_CREATION
