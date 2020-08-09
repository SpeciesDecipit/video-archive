import pytest

from server.apps.main.logic.tasks.download_video import download_video
from server.apps.main.models import VideoResource


@pytest.mark.django_db
def test_task_video_download(url_to_video: str, empty_video_resource: VideoResource):
    """Test checks video download task."""
    download_video(url_to_video, empty_video_resource.id)
    empty_video_resource.refresh_from_db()
    video_instance = empty_video_resource.videos.filter(primary=True).first()

    assert empty_video_resource.videos.all()
    assert video_instance.extension == 'mp4'
    assert video_instance.primary
    for item in video_instance.video.open():
        assert item
