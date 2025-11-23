from email.policy import default

from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from backend.db.models.base import BaseTable


class User(BaseTable):
    __tablename__ = 'users'

    login = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        doc="E-mail пользователя",
    )
    password = Column(
        String(255),
        nullable=False,
        doc="Пароль в зашифрованном виде",
    )
    project_id = Column(
        UUID(as_uuid=True),
        index=True,
        nullable=False,
        doc="UUID проекта, к которому прикреплен пользователь",
    )
    env = Column(
        Enum('prod', 'preprod', 'stage', name='env_enum'),
        nullable=False,
        doc="Название окружения (prod, preprod, stage)",
    )
    domain = Column(
        Enum('canary', 'regular', name='canary_enum'),
        nullable=False,
        default='canary',
        doc = "Тип пользователя (canary, regular)",
    )
    locktime = Column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        doc="Время наложения блокировки (TimeStamp)"
    )
