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


class authtoken(Base):
    __tablename__ = "authtoken"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4())
    token = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), index=True)
