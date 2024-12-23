from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    cpf: Mapped[str] = mapped_column(unique=True)
    phone_number: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    events: Mapped[Optional[List['Event']]] = relationship(
        'Event', back_populates='user', default_factory=list
    )


@table_registry.mapped_as_dataclass
class Event:
    __tablename__ = 'Events'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    image: Mapped[str]
    description: Mapped[str]
    location: Mapped[str]
    date: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    likes: Mapped[int] = mapped_column(init=False, default=0)
    user: Mapped[User] = relationship(
        'User', back_populates='events', init=False
    )

    # class TagsEvento (str, Enum):
    #     educacao = 'educacao'
    #     saude = 'saude'
    #     doacao = 'doacao'
