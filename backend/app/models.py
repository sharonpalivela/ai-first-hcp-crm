from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.db import Base

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)

    hcp_name = Column(String, nullable=True)
    interaction_type = Column(String, nullable=True)
    interaction_date = Column(DateTime, default=datetime.now)

    products_discussed = Column(Text, nullable=True)
    topics_discussed = Column(Text, nullable=True)

    materials_shared = Column(Text, nullable=True)
    samples_distributed = Column(Text, nullable=True)

    sentiment = Column(String, nullable=True)

    outcomes = Column(Text, nullable=True)
    objections = Column(Text, nullable=True)

    follow_up_action = Column(Text, nullable=True)
    follow_up_date = Column(String, nullable=True)

    summary = Column(Text, nullable=True)

    compliance_risk = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.now)