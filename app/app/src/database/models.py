from datetime import datetime
from sqlalchemy import String, Column, DateTime, Text, ForeignKey, MetaData
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import declarative_base, relationship
from uuid import uuid4

Base = declarative_base(metadata=MetaData())


class BaseModel(Base):
    __abstract__ = True

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    created_at = Column(DateTime(), default=datetime.now(), onupdate=datetime.now())


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String(255), unique=True, nullable=False)
    access_token = Column(postgresql.UUID(as_uuid=True), nullable=False, unique=True)

    audios = relationship("Audio", back_populates="user", cascade="all, delete-orphan")


class Audio(BaseModel):
    __tablename__ = "audios"

    user_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    filename = Column(Text, nullable=False)
    mp3_path = Column(Text, nullable=False)

    user = relationship("User", back_populates="audios")
