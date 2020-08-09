import pytest

from server.apps.main.logic.tasks.recoding import recode_video
from server.apps.main.models import VideoResource


@pytest.mark.django_db
def test_recoding(video_resource: VideoResource):
    """Test checks video recoding."""
    recode_video(video_resource.id, 'mkv')
    video_resource.refresh_from_db()
    video_instance = video_resource.videos.filter(extension='mkv').first()

    assert video_instance.video.open()
    assert not video_instance.primary
