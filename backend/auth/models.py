# T012, T016, T022: Pydantic Models for Authentication
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from enum import Enum


class SoftwareExpLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"


class HardwareExpLevel(str, Enum):
    NONE = "none"
    ARDUINO_RPI = "arduino_rpi"
    JETSON_INDUSTRIAL = "jetson_industrial"


class RoboticsBg(str, Enum):
    STUDENT = "student"
    HOBBYIST = "hobbyist"
    PROFESSIONAL = "professional"


# ============================================
# T012: User Registration Models
# ============================================
class UserCreate(BaseModel):
    """Request model for user registration."""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    name: Optional[str] = Field(None, max_length=255)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class UserResponse(BaseModel):
    """Response model for user data (no password)."""
    id: UUID
    email: str
    name: Optional[str]
    created_at: datetime
    profile_required: bool = True

    class Config:
        from_attributes = True


class UserWithProfile(BaseModel):
    """User response with profile status."""
    id: UUID
    email: str
    name: Optional[str]
    created_at: datetime
    has_profile: bool = False

    class Config:
        from_attributes = True


# ============================================
# T016: User Profile Models
# ============================================
class UserProfileCreate(BaseModel):
    """Request model for creating user profile."""
    software_exp: SoftwareExpLevel = SoftwareExpLevel.INTERMEDIATE
    hardware_exp: HardwareExpLevel = HardwareExpLevel.NONE
    robotics_bg: RoboticsBg = RoboticsBg.STUDENT
    languages: List[str] = Field(default=["python"])
    learning_goals: Optional[str] = Field(None, max_length=1000)


class UserProfileUpdate(BaseModel):
    """Request model for updating user profile (partial updates allowed)."""
    software_exp: Optional[SoftwareExpLevel] = None
    hardware_exp: Optional[HardwareExpLevel] = None
    robotics_bg: Optional[RoboticsBg] = None
    languages: Optional[List[str]] = None
    learning_goals: Optional[str] = Field(None, max_length=1000)


class UserProfileResponse(BaseModel):
    """Response model for user profile."""
    id: UUID
    user_id: UUID
    software_exp: str
    hardware_exp: str
    robotics_bg: str
    languages: List[str]
    learning_goals: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================
# T022: Login/Authentication Models
# ============================================
class LoginRequest(BaseModel):
    """Request model for user login."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Response model for authentication token."""
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
    user: UserResponse


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    message: str
