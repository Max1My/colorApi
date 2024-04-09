from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import EmailType, PasswordType

from src.db.engine import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = Column(
        PasswordType(
            schemes=["pbkdf2_sha512", "md5_crypt"],
            deprecated=["md5_crypt"]
        )
    )
