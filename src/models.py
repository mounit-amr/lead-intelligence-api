from sqlalchemy import Column, Integer, String, Float, Boolean
from database import base

class leadDB(base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    id = Column(Integer, primary_key=True, index=True)

    lead_id = Column(String, unique=True, index=True)

    company = Column(String)
    industry = Column(String)
    employees = Column(Integer)
    country = Column(String)

    revenue = Column(Float)
    funding = Column(Float)

    score = Column(Float, nullable=True)
    probability = Column(Float, nullable=True)
    classification = Column(String, nullable=True)

    converted = Column(Boolean, nullable=True)