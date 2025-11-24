from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class BaseTable(Base):
    __abstract__ = True

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True,
        doc="Уникальный идентификатор строки (UUID)",
    )

    dt_created = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        doc="Время появления записи (TimeStamp)"
    )
