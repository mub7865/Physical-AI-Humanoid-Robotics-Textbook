# API Contract: User Profile

**Feature**: 009-bonus-features
**Base Path**: `/api/profile`
**Date**: 2025-12-17

---

## Endpoints

### GET /api/profile

Get current user's profile.

**Headers Required**:
```
Authorization: Bearer <token>
```

**Response (200 OK)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "software_exp": "intermediate",
  "hardware_exp": "arduino_rpi",
  "robotics_bg": "student",
  "languages": ["python", "cpp"],
  "learning_goals": "Learn to build humanoid robots",
  "created_at": "2025-12-17T10:30:00Z",
  "updated_at": "2025-12-17T10:30:00Z"
}
```

**Response (404 Not Found)** - No profile exists:
```json
{
  "error": "PROFILE_NOT_FOUND",
  "message": "User profile not found. Please complete your profile."
}
```

**Errors**:
| Status | Code | Description |
|--------|------|-------------|
| 401 | UNAUTHORIZED | No valid session |
| 404 | PROFILE_NOT_FOUND | Profile not created yet |

---

### POST /api/profile

Create user profile (after signup).

**Headers Required**:
```
Authorization: Bearer <token>
```

**Request**:
```json
{
  "software_exp": "intermediate",
  "hardware_exp": "arduino_rpi",
  "robotics_bg": "student",
  "languages": ["python", "cpp"],
  "learning_goals": "Learn to build humanoid robots"
}
```

**Field Validation**:

| Field | Type | Required | Values |
|-------|------|----------|--------|
| software_exp | string | Yes | beginner, intermediate, expert |
| hardware_exp | string | Yes | none, arduino_rpi, jetson_industrial |
| robotics_bg | string | Yes | student, hobbyist, professional |
| languages | string[] | No | Any (common: python, cpp, ros, javascript) |
| learning_goals | string | No | Free text, max 1000 chars |

**Response (201 Created)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "software_exp": "intermediate",
  "hardware_exp": "arduino_rpi",
  "robotics_bg": "student",
  "languages": ["python", "cpp"],
  "learning_goals": "Learn to build humanoid robots",
  "created_at": "2025-12-17T10:30:00Z"
}
```

**Errors**:
| Status | Code | Description |
|--------|------|-------------|
| 400 | INVALID_SOFTWARE_EXP | Invalid software experience level |
| 400 | INVALID_HARDWARE_EXP | Invalid hardware experience level |
| 400 | INVALID_ROBOTICS_BG | Invalid robotics background |
| 401 | UNAUTHORIZED | No valid session |
| 409 | PROFILE_EXISTS | Profile already exists, use PUT |

---

### PUT /api/profile

Update existing user profile.

**Headers Required**:
```
Authorization: Bearer <token>
```

**Request** (partial update allowed):
```json
{
  "software_exp": "expert",
  "languages": ["python", "cpp", "ros"]
}
```

**Response (200 OK)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "software_exp": "expert",
  "hardware_exp": "arduino_rpi",
  "robotics_bg": "student",
  "languages": ["python", "cpp", "ros"],
  "learning_goals": "Learn to build humanoid robots",
  "updated_at": "2025-12-17T11:00:00Z"
}
```

**Side Effects**:
- Invalidates personalized content cache for this user

**Errors**:
| Status | Code | Description |
|--------|------|-------------|
| 400 | INVALID_FIELD | Invalid field value |
| 401 | UNAUTHORIZED | No valid session |
| 404 | PROFILE_NOT_FOUND | No profile to update |

---

## Profile Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    SIGNUP FLOW                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────┐     ┌─────────────┐     ┌────────────────┐   │
│   │ Signup  │────>│ Login Auto  │────>│ Profile Form   │   │
│   │ Form    │     │             │     │ (Questions)    │   │
│   └─────────┘     └─────────────┘     └───────┬────────┘   │
│                                               │             │
│                                               ▼             │
│                                       ┌────────────────┐   │
│                                       │ POST /profile  │   │
│                                       └───────┬────────┘   │
│                                               │             │
│                                               ▼             │
│                                       ┌────────────────┐   │
│                                       │  Dashboard     │   │
│                                       │  (Personalize) │   │
│                                       └────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Background Questions UI Mapping

| Question | Field | Options |
|----------|-------|---------|
| "What is your software development experience?" | software_exp | Beginner (just starting), Intermediate (some projects), Expert (professional) |
| "What is your hardware/electronics experience?" | hardware_exp | None (software only), Arduino/Raspberry Pi level, Jetson/Industrial level |
| "What is your robotics background?" | robotics_bg | Student (learning), Hobbyist (personal projects), Professional (work experience) |
| "Which programming languages do you know?" | languages | Multi-select: Python, C++, ROS, JavaScript, Other |
| "What are your learning goals?" (optional) | learning_goals | Free text input |
