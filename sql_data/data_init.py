
from app.db.models.models import Server
from app.db.session import SessionLocal

initial_data = [
    {"host": "sftp", "port": 22, "username": "testuser", "password": "password", "path": "upload"},    # noqa E501
    {"host": "sftp", "port": 22, "username": "testuser", "password": "password", "path": "upload"},  # noqa E501
]


def init():
    with SessionLocal() as session:
        for item in initial_data:
            session.add(Server(**item))
        session.commit()


if __name__ == "__main__":
    init()
