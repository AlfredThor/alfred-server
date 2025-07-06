from celery import Celery
from settings.env import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD


class CeleryApp:
    def __init__(self):
        self.app = Celery(
            'import_tasks',
            broker=f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/5',
            backend=f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/6'
        )
        self._configure()

    def _configure(self):
        self.app.conf.broker_transport_options = {'visibility_timeout': 3600}
        self.app.conf.task_serializer = 'json'
        self.app.conf.result_serializer = 'json'
        self.app.conf.accept_content = ['json']
        self.app.conf.timezone = 'Asia/Shanghai'
        self.app.conf.enable_utc = False

    def get_app(self) -> Celery:
        return self.app


# 实例化并导出 app 供其他模块使用
celery_app = CeleryApp().get_app()
celery_app.autodiscover_tasks(["tasks"])