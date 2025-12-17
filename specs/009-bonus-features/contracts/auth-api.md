# API Contract: Authentication

**Feature**: 009-bonus-features
**Base Path**: `/auth`
**Date**: 2025-12-17

---

## Endpoints

### POST /auth/signup

Create a new user account.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe"
}
```

**Response (201 Created)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2025-12-17T10:30:00Z",
  "profile_required": true
}
```

**Errors**:
| Status | Code | Description |
|--------|------|-------------|
| 400 | INVALID_EMAIL | Invalid email format |
| 400 | WEAK_PASSWORD | Password less than 8 characters |
| 409 | EMAIL_EXISTS | Email already registered |

---

### POST /auth/signin

Authenticate user and create session.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_at": "2025-12-24T10:30:00Z",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**Headers Set**:
```
Set-Cookie: auth_token=eyJhbG...; HttpOnly; Secure; SameSite=Lax; Max-Age=604800
```

**Errors**:
| Status | Code | Description |
|--------|------|-------------|
| 401 | INVALID_CREDENTIALS | Email or password incorrect |
| 429 | TOO_MANY_ATTEMPTS | Rate limited (5 attempts/minute) |

---

### POST /auth/signout

End user session.

**Headers Required**:
```
Authorization: Bearer <token>
```
or
```
Cookie: auth_token=<token>
```

**Response (200 OK)**:
```json
{
  "message": "Successfully signed out"
}
```

**Headers Set**:
```
Set-Cookie: auth_token=; HttpOnly; Secure; SameSite=Lax; Max-Age=0
```

**Errors**:
| Status | Code | Description |
|--------|------|-------------|
| 401 | UNAUTHORIZED | No valid session |

---

### GET /auth/me

Get current authenticated user.

**Headers Required**:
```
Authorization: Bearer <token>
```

**Response (200 OK)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2025-12-17T10:30:00Z",
  "has_profile": true
}
```

**Errors**:
| Status | Code | Description |
|--------|------|-------------|
| 401 | UNAUTHORIZED | No valid session |
| 401 | SESSION_EXPIRED | Session has expired |

---

## Authentication Flow

```
┌─────────┐                 ┌─────────┐                 ┌─────────┐
│ Client  │                 │ Backend │                 │   DB    │
└────┬────┘                 └────┬────┘                 └────┬────┘
     │                           │                           │
     │  POST /auth/signup        │                           │
     │ ─────────────────────────>│                           │
     │                           │  INSERT INTO users        │
     │                           │ ─────────────────────────>│
     │                           │                           │
     │  201 Created              │<─────────────────────────-│
     │ <─────────────────────────│                           │
     │                           │                           │
     │  POST /auth/signin        │                           │
     │ ─────────────────────────>│                           │
     │                           │  Verify credentials       │
     │                           │ ─────────────────────────>│
     │                           │                           │
     │                           │  INSERT INTO sessions     │
     │                           │ ─────────────────────────>│
     │                           │                           │
     │  200 OK + Set-Cookie      │<─────────────────────────-│
     │ <─────────────────────────│                           │
     │                           │                           │
     │  GET /auth/me             │                           │
     │  (with Cookie)            │                           │
     │ ─────────────────────────>│                           │
     │                           │  Validate token           │
     │                           │ ─────────────────────────>│
     │                           │                           │
     │  200 OK (user data)       │<─────────────────────────-│
     │ <─────────────────────────│                           │
     │                           │                           │
```

---

## Security Considerations

1. **Password Hashing**: Use bcrypt with cost factor 12
2. **Token Storage**: Store hashed tokens in DB, not plaintext
3. **HTTPS Only**: Cookies marked Secure, require HTTPS
4. **Rate Limiting**: 5 login attempts per minute per IP
5. **Session Expiry**: 7 days, configurable
