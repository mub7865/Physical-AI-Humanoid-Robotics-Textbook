# API Contract: Roman Urdu Translation

**Feature**: 009-bonus-features
**Base Path**: `/api/translate`
**Date**: 2025-12-17

---

## Endpoints

### POST /api/translate

Translate chapter content to Roman Urdu.

**Headers Required**:
```
Authorization: Bearer <token>  (Optional - works for guests too)
```

**Request**:
```json
{
  "chapter_id": "chapter-2-ros2",
  "content": "# ROS 2 Fundamentals\n\nROS 2 (Robot Operating System 2) is a set of software libraries...",
  "target_language": "roman_urdu",
  "use_cache": true
}
```

**Request Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| chapter_id | string | Yes | Chapter slug/identifier |
| content | string | Yes | Original chapter content (Markdown) |
| target_language | string | Yes | Only "roman_urdu" supported currently |
| use_cache | boolean | No | Use cached version if available (default: true) |

**Response (200 OK)**:
```json
{
  "chapter_id": "chapter-2-ros2",
  "original_hash": "a1b2c3d4e5f6...",
  "translated_content": "# ROS 2 Fundamentals\n\nROS 2 (Robot Operating System 2) software libraries ka ek set hai...",
  "source_language": "en",
  "target_language": "roman_urdu",
  "technical_terms_preserved": ["ROS 2", "Robot Operating System", "nodes", "topics", "Python"],
  "cached": false,
  "processing_time_ms": 4200
}
```

**Response (200 OK) - Cached**:
```json
{
  "chapter_id": "chapter-2-ros2",
  "original_hash": "a1b2c3d4e5f6...",
  "translated_content": "# ROS 2 Fundamentals\n\n...",
  "source_language": "en",
  "target_language": "roman_urdu",
  "cached": true,
  "cache_created_at": "2025-12-17T10:30:00Z"
}
```

**Errors**:
| Status | Code | Description |
|--------|------|-------------|
| 400 | MISSING_CONTENT | Content field is required |
| 400 | CONTENT_TOO_LARGE | Content exceeds 50KB limit |
| 400 | UNSUPPORTED_LANGUAGE | Only roman_urdu supported |
| 503 | AI_SERVICE_ERROR | OpenAI API temporarily unavailable |
| 504 | TIMEOUT | Translation took too long (>45s) |

---

### GET /api/translate/languages

Get list of supported target languages.

**Response (200 OK)**:
```json
{
  "supported_languages": [
    {
      "code": "roman_urdu",
      "name": "Roman Urdu",
      "description": "Urdu written in Latin/English alphabet"
    }
  ],
  "default_source": "en"
}
```

---

## Translation Logic

### Processing Pipeline

```
┌───────────────────┐
│  Original Content │
│    (English)      │
└─────────┬─────────┘
          │
          ▼
┌───────────────────────────────────────┐
│        Technical Term Extraction       │
│  Identify: ROS, Python, API, etc.     │
└─────────┬─────────────────────────────┘
          │
          ▼
┌───────────────────────────────────────┐
│           OpenAI GPT-4                │
│  Prompt: "Translate to Roman Urdu    │
│   keeping technical terms in English" │
└─────────┬─────────────────────────────┘
          │
          ▼
┌───────────────────────────────────────┐
│         Post-Processing               │
│  - Verify technical terms preserved   │
│  - Fix formatting issues              │
└─────────┬─────────────────────────────┘
          │
          ▼
┌───────────────────┐
│ Translated Content│
│   (Roman Urdu)    │
└───────────────────┘
```

---

## Technical Terms Preservation

### Categories of Terms to Keep in English

| Category | Examples |
|----------|----------|
| Programming Languages | Python, C++, JavaScript, ROS |
| Frameworks/Libraries | FastAPI, React, OpenAI SDK |
| Technical Acronyms | API, SDK, GPU, CPU, SLAM, URDF |
| Brand Names | NVIDIA, Intel, OpenAI, Ubuntu |
| Robotics Terms | node, topic, service, action, publisher, subscriber |
| Hardware Components | LiDAR, IMU, camera, sensor, actuator |
| File Formats | .py, .cpp, .urdf, .yaml, .json |

### Preservation Rules

1. **Keep English**: All items in categories above
2. **Translate**: Explanatory text, descriptions, analogies
3. **Hybrid**: Sentences mixing both (e.g., "ROS 2 mein nodes use hote hain")

---

## Example Translations

### Example 1: Simple Paragraph

**English**:
```markdown
ROS 2 (Robot Operating System 2) is the next generation of ROS.
It provides a flexible framework for writing robot software.
```

**Roman Urdu**:
```markdown
ROS 2 (Robot Operating System 2) ROS ki next generation hai.
Ye robot software likhne ke liye ek flexible framework provide karta hai.
```

---

### Example 2: Code Block (Preserved)

**English**:
```markdown
Here's how to create a simple publisher node:

```python
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
```
```

**Roman Urdu**:
```markdown
Yahan ek simple publisher node banana ka tareeqa hai:

```python
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
```
```

---

### Example 3: Technical List

**English**:
```markdown
## Key Components

- **Nodes**: Individual processes that perform computation
- **Topics**: Named buses for message passing
- **Services**: Request/response communication pattern
```

**Roman Urdu**:
```markdown
## Key Components

- **Nodes**: Individual processes jo computation perform karte hain
- **Topics**: Message passing ke liye named buses
- **Services**: Request/response communication pattern
```

---

## Caching Strategy

### Public Cache (user_id = NULL)
- Translations are public (same for everyone)
- Cached globally, not per-user
- Invalidated when original content changes

### Cache Lookup
```sql
SELECT cached_content FROM content_cache
WHERE chapter_id = ?
  AND content_type = 'translated'
  AND language = 'roman_urdu'
  AND original_hash = ?
  AND expires_at > NOW()
  AND user_id IS NULL;  -- Public cache
```

---

## Rate Limiting

| User Type | Limit |
|-----------|-------|
| Guest | 5 translations/hour |
| Authenticated | 20 translations/hour |

**Response (429 Too Many Requests)**:
```json
{
  "error": "RATE_LIMITED",
  "message": "Translation limit exceeded. Please try again later.",
  "retry_after": 3600
}
```

---

## Quality Assurance

### Translation Quality Checks
1. Technical terms remain unchanged
2. Markdown formatting preserved
3. Code blocks untouched
4. Links preserved
5. No mixed scripts (pure Roman Urdu, no Urdu script)

### Sample Quality Prompt
```
Translate to Roman Urdu (Urdu in Latin alphabet, NOT Urdu script).

Rules:
1. Keep ALL technical terms in English: {technical_terms_list}
2. Use simple, conversational Roman Urdu
3. Preserve ALL formatting (headings, lists, code blocks)
4. Do NOT translate code examples
5. Do NOT use Urdu script (نستعلیق) - only Latin alphabet

Content:
{content}
```
