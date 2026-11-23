
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    summary = Column(Text)
    verdict = Column(String)
    processed_at = Column(DateTime(timezone=True), server_default=func.now())

    pull_request_id = Column(
        Integer,
        ForeignKey("pull_requests.id")
    )

    pull_request = relationship(
        "PullRequest",
        back_populates="reviews"
    )

    findings = relationship(
        "Finding",
        back_populates="review"
    )
