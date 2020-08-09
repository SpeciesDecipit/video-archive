from django.conf import settings
from django.db.models import (
    Model,
    CharField,
    FileField,
    TextChoices,
    ForeignKey,
    CASCADE,
    BooleanField,
)
from typing_extensions import final


@final
class Status(TextChoices):
    """Enum for Video`s status field.

    Attrs:
        UPLOADING: Video uploading
        PREVIEW_CREATION: Video preview creation
        RECODING: Recording
        READY: Video is ready

    """

    UPLOADING = 'uploading'
    PREVIEW_CREATION = 'preview_creation'
    RECODING = 'recoding'
    READY = 'ready'


@final
class VideoResource(Model):
    """Django model representing a video resource."""

    title = CharField(max_length=128)
    preview = FileField(upload_to=settings.PREVIEW_PREFIX, blank=True, null=True)
    status = CharField(max_length=16, choices=Status.choices, default=Status.UPLOADING)

    def __str__(self) -> str:
        """Method string representation of VideoResource instance."""
        return f'{self.id}. {self.title}'


class Video(Model):
    """Django model representing a single video in the particular format."""

    video = FileField(upload_to=settings.VIDEO_PREFIX, blank=True, null=True)
    extension = CharField(max_length=16)
    video_resource = ForeignKey(VideoResource, related_name='videos', on_delete=CASCADE)
    primary = BooleanField(default=False)

    def __str__(self) -> str:
        """Method string representation of Video instance."""
        return f'{self.id}. {self.video_resource.title} - {self.extension}'
