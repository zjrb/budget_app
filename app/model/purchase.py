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


class Purchase(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    item = Column(String)
    cost = Column(Integer)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), index=True)
