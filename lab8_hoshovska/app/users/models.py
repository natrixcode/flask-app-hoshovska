from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        String(80),
        unique=True,
        nullable=False,
    )

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user",
    )

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"
