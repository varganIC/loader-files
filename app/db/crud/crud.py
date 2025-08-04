from typing import (
    List,
    Optional,
    Tuple
)

from sqlalchemy.orm import Session

from app.db.models.models import File, Server


def get_servers(db: Session) -> List[Server]:
    return (
        db.query(Server)
        .filter(Server.is_active.is_(True))
        .all()
    )


def get_server(db: Session, server_id: int) -> Optional[Server]:
    return (
        db.query(Server)
        .filter(Server.id == server_id)
        .first()
    )


def get_files_for_server(db: Session, server_id: int) -> List[Tuple[str]]:
    return (
        db.query(File.name)
        .filter(File.server_id == server_id)
        .all()
    )


def create_file(
    db: Session,
    name: str,
    server_id: int,
    processed: bool,
    uploaded: bool
) -> File:
    db_object = File(
        name=name,
        server_id=server_id,
        processed=processed,
        uploaded=uploaded
    )
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object
