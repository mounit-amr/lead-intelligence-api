from pydantic import BaseModel, Field

class Lead(BaseModel):
    lead_id: str
    company: str
    industry: str
    employees: int = Field(gt = 0)
    country: str
    revenue: float = Field(gt = 0)
    funding: float = Field(ge = 0)
    
