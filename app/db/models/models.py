from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Text,
    func
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from app.db.models.common import Base


class Server(Base):
    __tablename__ = 'server'

    id = Column(Integer, primary_key=True)
    host = Column(Text, nullable=False)
    port = Column(Integer, server_default=expression.literal(22))
    username = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    path = Column(Text, nullable=False)
    is_active = Column(Boolean, server_default=expression.true())

    files = relationship("File", back_populates="server")


class File(Base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    processed = Column(Boolean, server_default=expression.false())
    uploaded = Column(Boolean, server_default=expression.false())
    server_id = Column(
        Integer,
        ForeignKey('server.id'),
        index=True,
        nullable=False
    )
    created_at = Column(DateTime, server_default=func.now())
    exception = Column(Text, nullable=True)

    server = relationship("Server", back_populates="files")
