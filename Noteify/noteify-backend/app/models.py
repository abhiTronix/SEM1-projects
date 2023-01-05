from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql.expression import text
from .database import Base


class Files(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, nullable=False)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    subject_code = Column(String, nullable=False)
    published = Column(Boolean, server_default="FALSE", nullable=False)
    owner_username = Column(
        String, ForeignKey("users.username", ondelete="CASCADE"), nullable=False
    )
    owner = relationship("User")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    subject_code = Column(String, nullable=False)
    curr_version = Column(String, nullable=False)
    revision = Column(ARRAY(String))
    published = Column(Boolean, server_default="FALSE", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_username = Column(
        String, ForeignKey("users.username", ondelete="CASCADE"), nullable=False
    )
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    role = Column(String, server_default="ROLE_USER")


class Moderator(Base):
    __tablename__ = "moderators"
    username = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    uuid_pwd = Column(UUID, server_default=text("gen_random_uuid()"), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    role = Column(String, server_default="ROLE_MODERATOR")


class Vote(Base):
    __tablename__ = "votes"
    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    user_name = Column(
        String,
        ForeignKey("users.username", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
