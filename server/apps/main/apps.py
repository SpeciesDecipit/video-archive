from pathlib import Path

from django.apps import AppConfig
from django.conf import settings


class MainConfig(AppConfig):
    name = 'server.apps.main'

    def ready(self):
        Path(settings.VIDEO_ROOT).mkdir(parents=True, exist_ok=True)
        Path(settings.PREVIEW_ROOT).mkdir(parents=True, exist_ok=True)
