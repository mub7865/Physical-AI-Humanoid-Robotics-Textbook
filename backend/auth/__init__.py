# Authentication module for Better-Auth integration
from .routes import router as auth_router, profile_router, get_current_user, get_optional_user
from .models import (
    UserCreate, UserResponse, UserWithProfile,
    LoginRequest, TokenResponse,
    UserProfileCreate, UserProfileUpdate, UserProfileResponse,
    MessageResponse, ErrorResponse,
    SoftwareExpLevel, HardwareExpLevel, RoboticsBg
)
from .utils import (
    hash_password, verify_password,
    create_access_token, decode_access_token, hash_token
)

__all__ = [
    # Routers
    "auth_router",
    "profile_router",
    # Dependencies
    "get_current_user",
    "get_optional_user",
    # Models
    "UserCreate",
    "UserResponse",
    "UserWithProfile",
    "LoginRequest",
    "TokenResponse",
    "UserProfileCreate",
    "UserProfileUpdate",
    "UserProfileResponse",
    "MessageResponse",
    "ErrorResponse",
    # Enums
    "SoftwareExpLevel",
    "HardwareExpLevel",
    "RoboticsBg",
    # Utils
    "hash_password",
    "verify_password",
    "create_access_token",
    "decode_access_token",
    "hash_token"
]
