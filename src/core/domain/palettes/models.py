from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.mixins.models import PrimaryKeyMixin
from src.core.domain.users.models import User
from src.db.engine import Base


class Palette(Base, PrimaryKeyMixin):
    __tablename__ = 'palettes'
    name = Column(String)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id'),
        nullable=True
    )
    user: Mapped[User] = relationship(
        User,
        foreign_keys=[user_id],
        viewonly=True,
        lazy='joined'
    )
