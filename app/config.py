from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    temporal_address: str = "localhost:7233"
    temporal_namespace: str = "default"
    parent_task_queue: str = "parent-queue"
    child_task_queue: str = "child-queue"
    basic_auth_user: str = "admin"
    basic_auth_password: str = "changeme"


settings = Settings()
