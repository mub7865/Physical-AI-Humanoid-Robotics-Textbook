# Data Model: Hackathon Bonus Features

**Feature**: 009-bonus-features
**Date**: 2025-12-17
**Database**: Neon Serverless Postgres

---

## Entity Relationship Diagram

```
┌─────────────────────┐       ┌─────────────────────┐
│       users         │       │    user_profiles    │
├─────────────────────┤       ├─────────────────────┤
│ id (PK, UUID)       │──┐    │ id (PK, UUID)       │
│ email (UNIQUE)      │  │    │ user_id (FK, UNIQUE)│──┐
│ password_hash       │  │    │ software_exp        │  │
│ name                │  │    │ hardware_exp        │  │
│ created_at          │  │    │ robotics_bg         │  │
│ updated_at          │  │    │ languages (ARRAY)   │  │
└─────────────────────┘  │    │ learning_goals      │  │
                         │    │ created_at          │  │
                         │    │ updated_at          │  │
                         │    └─────────────────────┘  │
                         │                             │
                         │    ┌─────────────────────┐  │
                         │    │     sessions        │  │
                         │    ├─────────────────────┤  │
                         └───▶│ id (PK, UUID)       │  │
                              │ user_id (FK)        │  │
                              │ token_hash          │  │
                              │ expires_at          │  │
                              │ created_at          │  │
                              │ ip_address          │  │
                              │ user_agent          │  │
                              └─────────────────────┘  │
                                                       │
                              ┌─────────────────────┐  │
                              │   content_cache     │  │
                              ├─────────────────────┤  │
                              │ id (PK, UUID)       │  │
                              │ user_id (FK, NULL)  │◀─┘
                              │ chapter_id          │
                              │ content_type        │
                              │ language            │
                              │ original_hash       │
                              │ cached_content      │
                              │ created_at          │
                              │ expires_at          │
                              └─────────────────────┘

┌─────────────────────┐
│   chat_history      │  (EXISTING)
├─────────────────────┤
│ conversation_id (PK)│
│ user_message        │
│ bot_response        │
│ selected_text       │
│ timestamp           │
│ user_id (FK, NULL)  │  ← ADD THIS
└─────────────────────┘
```

---

## Table Definitions

### 1. users

Stores registered user accounts.

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, DEFAULT | Unique identifier |
| email | VARCHAR(255) | NOT NULL, UNIQUE | User's email address |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| name | VARCHAR(255) | NULLABLE | User's display name |
| email_verified | BOOLEAN | DEFAULT FALSE | Email verification status |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | Account creation time |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | Last update time |

---

### 2. user_profiles

Stores user background information for personalization.

```sql
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    software_exp VARCHAR(20) NOT NULL DEFAULT 'intermediate',
    hardware_exp VARCHAR(30) NOT NULL DEFAULT 'none',
    robotics_bg VARCHAR(20) NOT NULL DEFAULT 'student',
    languages TEXT[] DEFAULT ARRAY['python'],
    learning_goals TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT chk_software_exp CHECK (software_exp IN ('beginner', 'intermediate', 'expert')),
    CONSTRAINT chk_hardware_exp CHECK (hardware_exp IN ('none', 'arduino_rpi', 'jetson_industrial')),
    CONSTRAINT chk_robotics_bg CHECK (robotics_bg IN ('student', 'hobbyist', 'professional'))
);

CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
```

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| user_id | UUID | FK, UNIQUE, NOT NULL | Reference to users table |
| software_exp | VARCHAR(20) | NOT NULL, CHECK | beginner/intermediate/expert |
| hardware_exp | VARCHAR(30) | NOT NULL, CHECK | none/arduino_rpi/jetson_industrial |
| robotics_bg | VARCHAR(20) | NOT NULL, CHECK | student/hobbyist/professional |
| languages | TEXT[] | DEFAULT | Array of programming languages |
| learning_goals | TEXT | NULLABLE | Free-text learning objectives |
| created_at | TIMESTAMPTZ | DEFAULT | Profile creation time |
| updated_at | TIMESTAMPTZ | DEFAULT | Last update time |

---

### 3. sessions

Stores active user sessions for authentication.

```sql
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address VARCHAR(45),
    user_agent TEXT,

    CONSTRAINT chk_expires_future CHECK (expires_at > created_at)
);

CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_token_hash ON sessions(token_hash);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);
```

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Session identifier |
| user_id | UUID | FK, NOT NULL | Reference to users table |
| token_hash | VARCHAR(255) | NOT NULL | Hashed JWT token |
| expires_at | TIMESTAMPTZ | NOT NULL | Session expiration |
| created_at | TIMESTAMPTZ | DEFAULT | Session start time |
| ip_address | VARCHAR(45) | NULLABLE | Client IP (IPv4/IPv6) |
| user_agent | TEXT | NULLABLE | Client user agent string |

---

### 4. content_cache

Caches personalized and translated content.

```sql
CREATE TABLE content_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    chapter_id VARCHAR(255) NOT NULL,
    content_type VARCHAR(20) NOT NULL,
    language VARCHAR(20) NOT NULL DEFAULT 'en',
    original_hash VARCHAR(64) NOT NULL,
    cached_content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() + INTERVAL '7 days',

    CONSTRAINT chk_content_type CHECK (content_type IN ('personalized', 'translated')),
    CONSTRAINT chk_language CHECK (language IN ('en', 'roman_urdu')),
    UNIQUE(user_id, chapter_id, content_type, language)
);

CREATE INDEX idx_content_cache_lookup ON content_cache(user_id, chapter_id, content_type, language);
CREATE INDEX idx_content_cache_expires ON content_cache(expires_at);
```

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Cache entry identifier |
| user_id | UUID | FK, NULLABLE | NULL for public translations |
| chapter_id | VARCHAR(255) | NOT NULL | Chapter identifier (slug) |
| content_type | VARCHAR(20) | NOT NULL, CHECK | personalized or translated |
| language | VARCHAR(20) | NOT NULL, CHECK | en or roman_urdu |
| original_hash | VARCHAR(64) | NOT NULL | MD5 hash of original content |
| cached_content | TEXT | NOT NULL | Cached content |
| created_at | TIMESTAMPTZ | DEFAULT | Cache creation time |
| expires_at | TIMESTAMPTZ | DEFAULT | Cache expiration (7 days) |

---

### 5. chat_history (MODIFY EXISTING)

Add user_id to associate chat history with logged-in users.

```sql
-- Migration to add user_id column
ALTER TABLE chat_history
ADD COLUMN user_id UUID REFERENCES users(id) ON DELETE SET NULL;

CREATE INDEX idx_chat_history_user_id ON chat_history(user_id);
```

---

## Validation Rules

### User Registration
- Email: Valid email format, max 255 chars
- Password: Minimum 8 characters
- Name: Optional, max 255 chars

### User Profile
- software_exp: Must be one of: beginner, intermediate, expert
- hardware_exp: Must be one of: none, arduino_rpi, jetson_industrial
- robotics_bg: Must be one of: student, hobbyist, professional
- languages: Array of strings, common values: python, cpp, ros, javascript

### Sessions
- Token expires: 7 days from creation
- Cleanup job: Delete expired sessions daily

### Content Cache
- TTL: 7 days
- Invalidate: When user profile changes (personalized) or original content changes

---

## State Transitions

### User Account States
```
[New] → [Registered] → [Verified] → [Active]
                                  ↓
                              [Deleted]
```

### Session States
```
[Created] → [Active] → [Expired]
                     ↓
                [Revoked]
```

### Cache Entry States
```
[Created] → [Valid] → [Expired] → [Deleted]
                   ↓
              [Invalidated]
```

---

## Migration Script

```sql
-- Full migration script for 009-bonus-features

-- 1. Create users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Create user_profiles table
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    software_exp VARCHAR(20) NOT NULL DEFAULT 'intermediate',
    hardware_exp VARCHAR(30) NOT NULL DEFAULT 'none',
    robotics_bg VARCHAR(20) NOT NULL DEFAULT 'student',
    languages TEXT[] DEFAULT ARRAY['python'],
    learning_goals TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT chk_software_exp CHECK (software_exp IN ('beginner', 'intermediate', 'expert')),
    CONSTRAINT chk_hardware_exp CHECK (hardware_exp IN ('none', 'arduino_rpi', 'jetson_industrial')),
    CONSTRAINT chk_robotics_bg CHECK (robotics_bg IN ('student', 'hobbyist', 'professional'))
);

-- 3. Create sessions table
CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address VARCHAR(45),
    user_agent TEXT
);

-- 4. Create content_cache table
CREATE TABLE IF NOT EXISTS content_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    chapter_id VARCHAR(255) NOT NULL,
    content_type VARCHAR(20) NOT NULL,
    language VARCHAR(20) NOT NULL DEFAULT 'en',
    original_hash VARCHAR(64) NOT NULL,
    cached_content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() + INTERVAL '7 days',
    CONSTRAINT chk_content_type CHECK (content_type IN ('personalized', 'translated')),
    CONSTRAINT chk_language CHECK (language IN ('en', 'roman_urdu')),
    UNIQUE(user_id, chapter_id, content_type, language)
);

-- 5. Modify existing chat_history table
ALTER TABLE chat_history
ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id) ON DELETE SET NULL;

-- 6. Create indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_token_hash ON sessions(token_hash);
CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON sessions(expires_at);
CREATE INDEX IF NOT EXISTS idx_content_cache_lookup ON content_cache(user_id, chapter_id, content_type, language);
CREATE INDEX IF NOT EXISTS idx_content_cache_expires ON content_cache(expires_at);
CREATE INDEX IF NOT EXISTS idx_chat_history_user_id ON chat_history(user_id);
```

---

## Pydantic Models (Python)

```python
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None

class UserResponse(BaseModel):
    id: UUID
    email: str
    name: Optional[str]
    created_at: datetime

class UserProfileCreate(BaseModel):
    software_exp: str = "intermediate"
    hardware_exp: str = "none"
    robotics_bg: str = "student"
    languages: List[str] = ["python"]
    learning_goals: Optional[str] = None

class UserProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    software_exp: str
    hardware_exp: str
    robotics_bg: str
    languages: List[str]
    learning_goals: Optional[str]

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
```
