from pydantic import BaseModel, Field

class Lead(BaseModel):
    lead_id: str
    company: str
    industry: str
    employees: int = Field(gt = 0)
    country: str
    revenue: float = Field(gt = 0)
    funding: float = Field(ge = 0)
    budget: float = Field(ge=0 )
    
class ICP(BaseModel):
    industries: list[str] = Field(default_factory=list)
    countries: list[str] = Field(default_factory=list)
    employees_min: int | None = None
    employees_max: int | None = None
    revenue_min: float | None = None
    funding_min: float | None = None
    budget_min: float | None = None
    
    industry_weight: int = Field(25, ge=0)
    country_weight: int = Field(15, ge=0)
    employees_min_weight: int = Field(15, ge=0)
    employees_max_weight: int = Field(10, ge=0)
    revenue_weight: int = Field(15, ge=0)
    funding_weight: int = Field(10, ge=0)
    budget_weight: int = Field(10, ge=0)