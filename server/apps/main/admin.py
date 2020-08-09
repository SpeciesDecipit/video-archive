from django.contrib import admin  # noqa: F401

from server.apps.main.models import VideoResource, Video

admin.site.register(VideoResource)
admin.site.register(Video)
