import logging

from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    temporal_address: str = "localhost:7233"
    temporal_namespace: str = "default"
    parent_task_queue: str = "parent-queue"
    child_task_queue: str = "child-queue"
    basic_auth_user: str = "admin"
    basic_auth_password: str = "changeme"
    log_level: str = "INFO"
    metrics_port: int = 9464


settings = Settings()
