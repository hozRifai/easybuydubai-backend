from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class PropertyType(str, Enum):
    APARTMENT = "apartment"
    VILLA = "villa"
    TOWNHOUSE = "townhouse"
    PENTHOUSE = "penthouse"

class FinancingStatus(str, Enum):
    CASH = "cash"
    PRE_APPROVED = "pre_approved"
    NEEDS_FINANCING = "needs_financing"
    UNSURE = "unsure"

class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    session_id: Optional[str] = None
    user_info: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    session_id: str
    response: str
    message_count: int
    lead_analysis: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class PropertyRequirements(BaseModel):
    property_type: Optional[PropertyType] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    locations: Optional[List[str]] = []
    bedrooms: Optional[int] = None
    timeline: Optional[str] = None
    financing_status: Optional[FinancingStatus] = None
    special_requirements: Optional[List[str]] = []

class Lead(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None  # Changed from EmailStr to str
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    requirements: Optional[PropertyRequirements] = None
    lead_score: Optional[int] = Field(None, ge=0, le=100)
    session_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None

class SessionInfo(BaseModel):
    id: str
    created_at: str
    message_count: int
    last_message: Optional[str] = None

class HealthCheck(BaseModel):
    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0.0"
    environment: str