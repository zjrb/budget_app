from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.session import Base
import uuid


class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4())
    firstname = Column(String)
    lastname = Column(String)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    