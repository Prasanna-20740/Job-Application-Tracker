
from pydantic import BaseModel
from typing import Optional


class JobSuggestion(BaseModel):
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    redirect_url: Optional[str] = None
    description: Optional[str] = None
