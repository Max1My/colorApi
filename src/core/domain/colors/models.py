from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from src.common.mixins.models import PrimaryKeyMixin

from src.core.domain.palettes.models import Palette
from src.db.engine import Base


class Color(Base, PrimaryKeyMixin):
    __tablename__ = 'colors'
    name = Column(String)
    hex_color = Column(String)
    palette_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('palettes.id'),
        nullable=True
    )
    palette: Mapped[Palette] = relationship(
        Palette,
        foreign_keys=[palette_id],
        viewonly=True,
        lazy='joined',
    )
