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


class Budget(Base):
    __tablename__ = "budget"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), index=True)
    start_budget = Column(Integer)
    curr_budget = Column(Integer)
