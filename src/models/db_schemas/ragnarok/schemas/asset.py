from .base_schema import SQLAlchemyBase
from sqlalchemy import Column, Integer, DateTime, func, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import Index
import uuid

class Asset(SQLAlchemyBase):
    __tablename__ = "assets"
    
    id         = Column(Integer, primary_key=True, autoincrement=True)
    uuid       = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    type       = Column(String, nullable=False)
    name       = Column(String, nullable=False)
    size       = Column(Integer, nullable=False)
    config     = Column(JSONB, nullable=True)
    saved_at   = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    project = relationship("Project", back_populates="assets")
    chunks  = relationship("Chunk", back_populates="asset")

    __table_args__ = (
        Index("ix_asset_project_id", project_id),
    )