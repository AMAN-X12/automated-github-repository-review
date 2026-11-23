
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    owner = Column(String, nullable=False)

    pull_requests = relationship(
        "PullRequest",
        back_populates="repository"
    )
