# T015, T017, T023, T024, T025: Authentication Routes
from fastapi import APIRouter, HTTPException, status, Depends, Response, Request, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from datetime import datetime, timezone

from .models import (
    UserCreate, UserResponse, UserWithProfile,
    LoginRequest, TokenResponse,
    UserProfileCreate, UserProfileUpdate, UserProfileResponse,
    MessageResponse, ErrorResponse
)
from .utils import (
    hash_password, verify_password,
    create_access_token, decode_access_token, hash_token
)
from database import (
    create_user, get_user_by_email, get_user_by_id,
    create_user_profile, get_user_profile, update_user_profile,
    create_session, get_session_by_token_hash, delete_session, delete_user_sessions,
    clear_user_cache
)

router = APIRouter(prefix="/auth", tags=["Authentication"])
profile_router = APIRouter(prefix="/api", tags=["Profile"])

security = HTTPBearer(auto_error=False)


# ============================================
# Authentication Dependencies
# ============================================
async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    auth_token: Optional[str] = Cookie(None)
) -> dict:
    """
    Extract and validate the current user from JWT token.
    Supports both Bearer token and cookie-based auth.
    """
    token = None

    # Check Bearer token first
    if credentials:
        token = credentials.credentials
    # Fallback to cookie
    elif auth_token:
        token = auth_token

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "UNAUTHORIZED", "message": "Not authenticated"}
        )

    # Decode token
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "UNAUTHORIZED", "message": "Invalid or expired token"}
        )

    # Verify session exists in database
    token_hash = hash_token(token)
    session = get_session_by_token_hash(token_hash)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "SESSION_EXPIRED", "message": "Session has expired"}
        )

    # Get user from database
    user = get_user_by_id(payload["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "UNAUTHORIZED", "message": "User not found"}
        )

    user["token"] = token
    user["token_hash"] = token_hash
    return user


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    auth_token: Optional[str] = Cookie(None)
) -> Optional[dict]:
    """Get current user if authenticated, None otherwise."""
    try:
        return await get_current_user(credentials, auth_token)
    except HTTPException:
        return None


# ============================================
# T015: POST /auth/signup - User Registration
# ============================================
@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        409: {"model": ErrorResponse, "description": "Email already exists"}
    }
)
async def signup(user_data: UserCreate):
    """
    Register a new user account.

    - **email**: Valid email address (unique)
    - **password**: Minimum 8 characters
    - **name**: Optional display name
    """
    # Check password length
    if len(user_data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "WEAK_PASSWORD", "message": "Password must be at least 8 characters"}
        )

    # Hash password
    password_hash = hash_password(user_data.password)

    # Create user
    user = create_user(
        email=user_data.email,
        password_hash=password_hash,
        name=user_data.name
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "EMAIL_EXISTS", "message": "Email already registered"}
        )

    return UserResponse(
        id=user["id"],
        email=user["email"],
        name=user["name"],
        created_at=user["created_at"],
        profile_required=True
    )


# ============================================
# T023: POST /auth/signin - User Login
# ============================================
@router.post(
    "/signin",
    response_model=TokenResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"}
    }
)
async def signin(login_data: LoginRequest, response: Response, request: Request):
    """
    Authenticate user and create session.

    Returns JWT token and sets HttpOnly cookie.
    """
    # Get user by email
    user = get_user_by_email(login_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "INVALID_CREDENTIALS", "message": "Email or password incorrect"}
        )

    # Verify password
    if not verify_password(login_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "INVALID_CREDENTIALS", "message": "Email or password incorrect"}
        )

    # Create JWT token
    token, expires_at = create_access_token(
        user_id=str(user["id"]),
        email=user["email"]
    )

    # Store session in database
    token_hash = hash_token(token)
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    create_session(
        user_id=str(user["id"]),
        token_hash=token_hash,
        expires_at=expires_at,
        ip_address=ip_address,
        user_agent=user_agent
    )

    # Set HttpOnly cookie
    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7 * 24 * 60 * 60  # 7 days
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_at=expires_at,
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            created_at=user["created_at"],
            profile_required=get_user_profile(str(user["id"])) is None
        )
    )


# ============================================
# T024: POST /auth/signout - User Logout
# ============================================
@router.post(
    "/signout",
    response_model=MessageResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"}
    }
)
async def signout(response: Response, current_user: dict = Depends(get_current_user)):
    """
    End user session and clear auth cookie.
    """
    # Delete session from database
    delete_session(current_user["token_hash"])

    # Clear cookie
    response.delete_cookie(
        key="auth_token",
        httponly=True,
        secure=True,
        samesite="lax"
    )

    return MessageResponse(message="Successfully signed out")


# ============================================
# T025: GET /auth/me - Get Current User
# ============================================
@router.get(
    "/me",
    response_model=UserWithProfile,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"}
    }
)
async def get_me(current_user: dict = Depends(get_current_user)):
    """
    Get current authenticated user information.
    """
    profile = get_user_profile(str(current_user["id"]))

    return UserWithProfile(
        id=current_user["id"],
        email=current_user["email"],
        name=current_user["name"],
        created_at=current_user["created_at"],
        has_profile=profile is not None
    )


# ============================================
# T017: Profile Endpoints
# ============================================
@profile_router.get(
    "/profile",
    response_model=UserProfileResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
        404: {"model": ErrorResponse, "description": "Profile not found"}
    }
)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """
    Get current user's profile.
    """
    profile = get_user_profile(str(current_user["id"]))

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "PROFILE_NOT_FOUND", "message": "User profile not found. Please complete your profile."}
        )

    return UserProfileResponse(**profile)


@profile_router.post(
    "/profile",
    response_model=UserProfileResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        401: {"model": ErrorResponse, "description": "Not authenticated"},
        409: {"model": ErrorResponse, "description": "Profile already exists"}
    }
)
async def create_profile(
    profile_data: UserProfileCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create user profile (after signup).

    - **software_exp**: beginner, intermediate, or expert
    - **hardware_exp**: none, arduino_rpi, or jetson_industrial
    - **robotics_bg**: student, hobbyist, or professional
    - **languages**: List of programming languages
    - **learning_goals**: Optional free text (max 1000 chars)
    """
    # Check if profile already exists
    existing = get_user_profile(str(current_user["id"]))
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "PROFILE_EXISTS", "message": "Profile already exists, use PUT to update"}
        )

    # Create profile
    profile = create_user_profile(
        user_id=str(current_user["id"]),
        software_exp=profile_data.software_exp.value,
        hardware_exp=profile_data.hardware_exp.value,
        robotics_bg=profile_data.robotics_bg.value,
        languages=profile_data.languages,
        learning_goals=profile_data.learning_goals
    )

    return UserProfileResponse(**profile)


@profile_router.put(
    "/profile",
    response_model=UserProfileResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        401: {"model": ErrorResponse, "description": "Not authenticated"},
        404: {"model": ErrorResponse, "description": "Profile not found"}
    }
)
async def update_profile(
    profile_data: UserProfileUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update user profile (partial updates allowed).

    Side effect: Invalidates personalized content cache for this user.
    """
    # Check if profile exists
    existing = get_user_profile(str(current_user["id"]))
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "PROFILE_NOT_FOUND", "message": "No profile to update"}
        )

    # Build update dict
    update_dict = {}
    if profile_data.software_exp is not None:
        update_dict["software_exp"] = profile_data.software_exp.value
    if profile_data.hardware_exp is not None:
        update_dict["hardware_exp"] = profile_data.hardware_exp.value
    if profile_data.robotics_bg is not None:
        update_dict["robotics_bg"] = profile_data.robotics_bg.value
    if profile_data.languages is not None:
        update_dict["languages"] = profile_data.languages
    if profile_data.learning_goals is not None:
        update_dict["learning_goals"] = profile_data.learning_goals

    # Update profile
    profile = update_user_profile(str(current_user["id"]), **update_dict)

    # Invalidate personalized content cache
    clear_user_cache(str(current_user["id"]))

    return UserProfileResponse(**profile)
