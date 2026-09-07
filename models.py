from database import Base

from sqlalchemy import Column, BigInteger, String, Text, Boolean, TIMESTAMP, Identity
from sqlalchemy.sql import func

class Todo(Base):
    __tablename__ = "todos"

    id = Column(
        BigInteger, 
        Identity(start=1, increment=1), 
        primary_key=True
    )
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    is_complete = Column(Boolean, nullable=False, server_default='FALSE')
    created_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, 
        server_default=func.now(), 
        onupdate=func.now()
    )