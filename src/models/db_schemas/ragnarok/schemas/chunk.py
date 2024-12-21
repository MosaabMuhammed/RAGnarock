from .base_schema import SQLAlchemyBase
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import Index
import uuid

class Chunk(SQLAlchemyBase):
    __tablename__ = "chunks"
    id         = Column(Integer, primary_key=True, autoincrement=True)
    uuid       = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    asset_id   = Column(Integer, ForeignKey("assets.id"), nullable=False)
    text       = Column(String, nullable=False)
    order      = Column(Integer, nullable=False)
    config     = Column(JSONB, nullable=True)

    project = relationship("Project", back_populates="chunks")
    asset   = relationship("Asset",   back_populates="chunks")


    __table_args__ = (
        Index("ix_chunk_project_id", project_id),
        Index("ix_chunk_asset_id", asset_id)

    )