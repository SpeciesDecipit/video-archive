import pytest
from django.core.files.base import ContentFile

from server.apps.main.models import VideoResource, Video


@pytest.fixture()
def url_to_video() -> str:
    """Fixture with url to video."""
    return (
        'https://file-examples-com.github.io/uploads/'
        + '2017/04/file_example_MP4_480_1_5MG.mp4'
    )


@pytest.fixture()
def empty_video_resource() -> VideoResource:
    """Fixture with empty VideoResource."""
    return VideoResource.objects.create(title='VideoResource')


@pytest.fixture()
def video_resource() -> VideoResource:
    """Fixture with VideoResource."""
    video_resource_instance = VideoResource.objects.create(title='VideoResource')
    video_instance = Video.objects.create(
        primary=True, video_resource=video_resource_instance, extension='mp4'
    )
    video_instance.video.save(
        'video.mp4', ContentFile(open('tests/assets/video.mp4', 'rb').read())
    )
    return video_resource_instance
