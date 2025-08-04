import json
import logging
import os

from app.celery_app import app
from app.clients.minio.minio_client import get_minio_client
from app.clients.rabbit_mq.rabbit_mq_client import get_rabbit_client
from app.clients.redis.redis_client import acquire_lock, release_lock
from app.clients.sftp.sftp_client import get_sftp_client
from app.db.crud import crud
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)


@app.task
def check_servers():
    logger.info("Запущена check_servers")
    with SessionLocal() as db:
        servers = crud.get_servers(db)
        for server in servers:
            logger.info(
                f"Запуск download_new_files "
                f"для сервера {server.id}"
            )
            download_new_files.delay(server.id)


@app.task
def download_new_files(server_id: int):
    logger.info(
        f"Задача download_new_files "
        f"запущена для {server_id}"
    )

    sftp, transport = None, None
    try:
        with SessionLocal() as db:
            server = crud.get_server(db, server_id)
            sftp, transport = get_sftp_client(
                server.host,
                server.port,
                server.username,
                server.password
            )
            existing_files = {
                row[0]
                for row in crud.get_files_for_server(db, server_id)
            }

            for file_attr in sftp.listdir_attr(server.path):
                filename = file_attr.filename
                if filename not in existing_files:
                    logger.info(
                        f"Запуск process_file "
                        f"для сервера {server.id} "
                        f"и файла: {filename}"
                    )
                    process_file.delay(server_id, filename)

    except Exception as e:
        logger.error(
            f"Ошибка download_new_files "
            f"для сервера {server_id}: {e}"
        )
        raise e
    finally:
        if sftp:
            sftp.close()
        if transport:
            transport.close()


@app.task
def process_file(server_id: int, filename: str):
    logger.info(
        f"Задача process_file запущена "
        f"для {server_id} и файла: {filename}"
    )

    db, sftp, transport, minio_client = None, None, None, None
    new_file = None
    lock_key = f"lock:file:{server_id}:{filename}"

    try:
        with SessionLocal() as db:
            if not acquire_lock(lock_key):
                logger.info(
                    f"Файл {filename} "
                    f"на сервере {server_id} "
                    f"уже обрабатывается"
                )
                return

            server = crud.get_server(db, server_id)
            sftp, transport = get_sftp_client(
                server.host,
                server.port,
                server.username,
                server.password
            )
            minio_client = get_minio_client()
            new_file = crud.create_file(
                db=db,
                name=filename,
                server_id=server_id,
                processed=True,
                uploaded=False
            )

            path_file_sftp = os.path.join(
                server.path, filename
            ).replace('\\', '/')

            path_file_minio = os.path.join(
                'server',
                str(server_id),
                filename
            ).replace('\\', '/')

            with sftp.open(path_file_sftp, 'rb') as sftp_file:
                minio_client.client.put_object(
                    bucket_name=minio_client.bucket,
                    object_name=path_file_minio,
                    data=sftp_file,
                    length=sftp.stat(path_file_sftp).st_size,
                )
            new_file.uploaded = True
            new_file.processed = False
            db.commit()

        notify_file_uploaded.delay(path_file_minio)

    except Exception as e:
        logger.error(
            f"Ошибка process_file для "
            f"сервера {server_id} "
            f"и файла {filename}: {e}"
        )
        db.rollback()
        if new_file:
            new_file = db.merge(new_file)
            new_file.exception = str(e)
            new_file.processed = False
            db.commit()
        raise e
    finally:
        if sftp:
            sftp.close()
        if transport:
            transport.close()
        if minio_client:
            del minio_client
        release_lock(lock_key)


@app.task
def notify_file_uploaded(path_file: str):
    logger.info(
        f"Задача notify_file_uploaded "
        f"запущена для файла: {path_file}"
    )

    with get_rabbit_client() as rabbit_mq:
        rabbit_mq.queue_declare()
        rabbit_mq.publish(
            json.dumps({'file': path_file}),
            'upload_in'
        )

# if __name__ == '__main__':
#     download_new_files(1)
