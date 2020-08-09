from __future__ import absolute_import, unicode_literals

from os import environ
from typing import List

from celery import Celery


class Config:
    broker_url: str = (
        f'amqp://{environ.get("RABBITMQ_DEFAULT_USER")}:'
        f'{environ.get("RABBITMQ_DEFAULT_PASS")}@'
        f'{environ.get("RABBITMQ_HOST")}:{environ.get("RABBITMQ_PORT")}/'
        f'{environ.get("RABBITMQ_DEFAULT_VHOST")}'
    )
    broker_api: str = (
        f'http://{environ.get("RABBITMQ_DEFAULT_USER")}:'
        f'{environ.get("RABBITMQ_DEFAULT_PASS")}@'
        f'{environ.get("RABBITMQ_HOST")}:{environ.get("RABBITMQ_PORT")}/api/'
    )
    imports: List[str] = [
        'server.apps.main.logic.tasks.create_preview',
        'server.apps.main.logic.tasks.download_video',
        'server.apps.main.logic.tasks.recoding',
        'server.apps.main.logic.tasks.pipelines',
        'server.apps.main.logic.tasks.video_resource_states',
    ]


app = Celery()
app.config_from_object(Config)
