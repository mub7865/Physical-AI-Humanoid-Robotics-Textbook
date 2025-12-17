# API Contract: Content Personalization

**Feature**: 009-bonus-features
**Base Path**: `/api/personalize`
**Date**: 2025-12-17

---

## Endpoints

### POST /api/personalize

Personalize chapter content based on user's background profile.

**Headers Required**:
```
Authorization: Bearer <token>
```

**Request**:
```json
{
  "chapter_id": "chapter-2-ros2",
  "content": "# ROS 2 Fundamentals\n\nROS 2 (Robot Operating System 2) is a set of software libraries...",
  "use_cache": true
}
```

**Request Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| chapter_id | string | Yes | Chapter slug/identifier |
| content | string | Yes | Original chapter content (Markdown) |
| use_cache | boolean | No | Use cached version if available (default: true) |

**Response (200 OK)**:
```json
{
  "chapter_id": "chapter-2-ros2",
  "original_hash": "a1b2c3d4e5f6...",
  "personalized_content": "# ROS 2 Fundamentals\n\nAgar aap Python se familiar hain, toh ROS 2 samajhna asaan hoga...",
  "profile_used": {
    "software_exp": "intermediate",
    "hardware_exp": "arduino_rpi",
    "robotics_bg": "student"
  },
  "cached": false,
  "processing_time_ms": 3500
}
```

**Response (200 OK) - Cached**:
```json
{
  "chapter_id": "chapter-2-ros2",
  "original_hash": "a1b2c3d4e5f6...",
  "personalized_content": "# ROS 2 Fundamentals\n\n...",
  "profile_used": {
    "software_exp": "intermediate",
    "hardware_exp": "arduino_rpi",
    "robotics_bg": "student"
  },
  "cached": true,
  "cache_created_at": "2025-12-17T10:30:00Z"
}
```

**Errors**:
| Status | Code | Description |
|--------|------|-------------|
| 400 | MISSING_CONTENT | Content field is required |
| 400 | CONTENT_TOO_LARGE | Content exceeds 50KB limit |
| 401 | UNAUTHORIZED | No valid session |
| 404 | PROFILE_NOT_FOUND | User profile required for personalization |
| 503 | AI_SERVICE_ERROR | OpenAI API temporarily unavailable |
| 504 | TIMEOUT | Personalization took too long (>30s) |

---

### DELETE /api/personalize/cache

Clear personalized content cache for current user.

**Headers Required**:
```
Authorization: Bearer <token>
```

**Request** (optional - clear specific chapter):
```json
{
  "chapter_id": "chapter-2-ros2"
}
```

**Response (200 OK)**:
```json
{
  "message": "Cache cleared successfully",
  "chapters_cleared": 5
}
```

---

## Personalization Logic

### Input Processing
```
┌───────────────────┐     ┌───────────────────┐
│  Original Content │     │   User Profile    │
│    (Markdown)     │     │  - software_exp   │
│                   │     │  - hardware_exp   │
│                   │     │  - robotics_bg    │
└─────────┬─────────┘     └─────────┬─────────┘
          │                         │
          └───────────┬─────────────┘
                      │
                      ▼
          ┌───────────────────┐
          │   OpenAI GPT-4    │
          │   with prompt:    │
          │   "Personalize    │
          │    for {profile}" │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │   Personalized    │
          │     Content       │
          └───────────────────┘
```

### Personalization Rules by Level

**Software Experience**:
| Level | Adjustments |
|-------|-------------|
| Beginner | Add code basics, explain syntax, use analogies |
| Intermediate | Standard explanations, some context |
| Expert | Skip basics, focus on advanced concepts, be concise |

**Hardware Experience**:
| Level | Adjustments |
|-------|-------------|
| None | Explain electronics basics, avoid hardware assumptions |
| Arduino/RPi | Reference familiar platforms, bridge concepts |
| Jetson/Industrial | Use professional terminology, assume knowledge |

**Robotics Background**:
| Level | Adjustments |
|-------|-------------|
| Student | Academic tone, theory focus, exercises |
| Hobbyist | Practical focus, project ideas, tips |
| Professional | Industry context, best practices, efficiency |

---

## Caching Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                    CACHE LOOKUP FLOW                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Request comes in                                          │
│         │                                                   │
│         ▼                                                   │
│   ┌─────────────┐                                          │
│   │ use_cache?  │──No──> Generate new content              │
│   └──────┬──────┘                                          │
│          │Yes                                               │
│          ▼                                                  │
│   ┌─────────────────┐                                      │
│   │ Check DB cache  │                                      │
│   │ WHERE user_id   │                                      │
│   │   AND chapter_id│                                      │
│   │   AND hash      │                                      │
│   └────────┬────────┘                                      │
│            │                                                │
│     ┌──────┴──────┐                                        │
│     │             │                                        │
│   Found?        Not Found                                  │
│     │             │                                        │
│     ▼             ▼                                        │
│  Return        Generate new                                │
│  cached        → Save to cache                             │
│  content       → Return                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Cache Invalidation Triggers
1. User updates profile → Clear all user's cached content
2. Original content changes (hash mismatch) → Regenerate
3. Cache expires (7 days TTL) → Regenerate on next request

---

## Example Personalization

**Original Content** (for chapter-2-ros2):
```markdown
## ROS 2 Nodes

A node is a fundamental building block in ROS 2. Each node is responsible
for a single, modular purpose. Nodes communicate using topics, services,
and actions.
```

**Personalized for Beginner + No Hardware**:
```markdown
## ROS 2 Nodes

Socho ROS 2 ko ek team ki tarah - har "node" ek team member hai jo
specific kaam karta hai. Jaise ek team mein ek person accounts dekhta hai
aur doosra marketing, waise hi ek node camera handle karta hai aur
doosra motors.

**Node kya hai?**
Ek node ek chota program hai jo ek kaam karta hai. For example:
- Camera node: Camera se images leta hai
- Motor node: Motors ko control karta hai

**Nodes baat kaise karte hain?**
Nodes ek doosre se "topics" ke through communicate karte hain -
ye WhatsApp groups jaisa hai jahan messages broadcast hote hain.
```

**Personalized for Expert + Jetson**:
```markdown
## ROS 2 Nodes

Nodes are process-isolated units in the ROS 2 computation graph.
Key considerations for Jetson deployment:

- **Memory footprint**: Each node spawns its own process; use
  component nodes for memory-constrained deployments
- **Real-time**: Configure SCHED_FIFO with appropriate priorities
- **IPC**: Prefer shared memory transport over loopback for
  intra-device communication

Communication primitives: Topics (pub/sub), Services (request/response),
Actions (long-running with feedback).
```
