import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_HOST: str = os.getenv("APP_HOST")
    APP_PORT: int = os.getenv("APP_PORT")

    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")

    RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST")
    RABBITMQ_PORT: int = os.getenv("RABBITMQ_PORT")
    RABBITMQ_DEFAULT_USER: str = os.getenv("RABBITMQ_DEFAULT_USER")
    RABBITMQ_DEFAULT_PASS: str = os.getenv("RABBITMQ_DEFAULT_PASS")
    RABBITMQ_VIRTUAL_HOST: str = os.getenv("RABBITMQ_VIRTUAL_HOST")

    MINIO_HOST: str = os.getenv("MINIO_HOST")
    MINIO_PORT: int = os.getenv("MINIO_PORT")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ROOT_USER")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_ROOT_PASSWORD")
    MINIO_SECURE: bool = False

    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = os.getenv("REDIS_PORT")

    def get_sync_database_url(self):
        return 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_HOST,
            self.POSTGRES_PORT,
            self.POSTGRES_DB
        )

    def get_connection_rabbit(self):
        return 'amqp://{0}:{1}@{2}:{3}{4}'.format(
            self.RABBITMQ_DEFAULT_USER,
            self.RABBITMQ_DEFAULT_PASS,
            self.RABBITMQ_HOST,
            self.RABBITMQ_PORT,
            self.RABBITMQ_VIRTUAL_HOST or '/',
        )

    def get_connection_minio(self):
        d = {
            'access_key': self.MINIO_ACCESS_KEY,
            'secret_key': self.MINIO_SECRET_KEY,
            'endpoint': f'{self.MINIO_HOST}:{self.MINIO_PORT}',
            'secure': self.MINIO_SECURE
        }
        return d


settings = Settings()
