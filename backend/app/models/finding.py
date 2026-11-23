
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    line_number = Column(Integer)
    severity = Column(String)
    category = Column(String)
    explanation = Column(Text)
    suggestion = Column(Text)

    review_id = Column(Integer, ForeignKey("reviews.id"))

    review = relationship(
        "Review",
        back_populates="findings"
    )
