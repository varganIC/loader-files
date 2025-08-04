from typing import Optional

from minio import Minio
from minio.error import MinioException

from app.config import settings


class MinioServerClient:
    def __init__(self, config: dict):
        self._settings = config
        self.client: Optional[Minio] = None
        self.bucket: str = 'uploads'

    def connect(self):
        try:
            self.client = Minio(**self._settings)
        except MinioException:
            self.client = None


def get_minio_client() -> MinioServerClient:
    client_wrapper = MinioServerClient(settings.get_connection_minio())
    client_wrapper.connect()
    if not client_wrapper.client:
        raise ConnectionError("MinIO недоступен")
    return client_wrapper
