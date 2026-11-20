from datetime import datetime, timezone
from sqlalchemy import (
    Enum,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
    Table,
    Column,
    Integer,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db

post_tags = Table(
    "post_tags",
    db.metadata,
    Column(
        "post_id",
        Integer,
        ForeignKey("post.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        Integer,
        ForeignKey("tag.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Tag(db.Model):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        secondary=post_tags,
        back_populates="tags",
    )

    def __repr__(self):
        return f"<Tag {self.id}: {self.name}>"


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
    )
    category: Mapped[str] = mapped_column(
        Enum("news", "publication", "tech", "other", name="post_category"),
        default="other",
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="1", nullable=False
    )
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("user.id", name="fk_post_user_id"),
        nullable=True,
    )

    user: Mapped["User | None"] = relationship(
        "User",
        back_populates="posts",
    )

    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary=post_tags,
        back_populates="posts",
    )

    def __repr__(self):
        return f"<Post {self.id}: {self.title}>"
