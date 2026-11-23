
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True, index=True)
    pr_number = Column(Integer, nullable=False)
    status = Column(String, default="pending")
    author = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    repository_id = Column(Integer, ForeignKey("repositories.id"))

    repository = relationship(
        "Repository",
        back_populates="pull_requests"
    )

    reviews = relationship(
        "Review",
        back_populates="pull_request"
    )
