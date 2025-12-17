# Research: Hackathon Bonus Features

**Feature**: 009-bonus-features
**Date**: 2025-12-17
**Purpose**: Resolve technical unknowns and establish best practices

---

## 1. Better-Auth Integration with FastAPI

### Decision: Use Better-Auth with custom FastAPI adapter

### Rationale:
- Better-Auth is a modern authentication library designed for TypeScript/JavaScript
- For Python/FastAPI backend, we need to implement the server-side logic manually
- Better-Auth provides client-side React hooks which we can use in Docusaurus

### Implementation Approach:
1. **Backend (FastAPI)**: Implement custom auth endpoints following Better-Auth patterns
   - Use `passlib` for password hashing (bcrypt)
   - Use `python-jose` for JWT token generation
   - Store sessions in Neon Postgres

2. **Frontend (React)**: Use Better-Auth React client
   - Install `better-auth` npm package
   - Configure to point to our FastAPI endpoints

### Alternatives Considered:
| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Better-Auth (full) | Modern, hackathon requirement | No Python SDK | ✅ Use client + custom backend |
| NextAuth.js | Well documented | Wrong framework | ❌ Rejected |
| Custom JWT | Full control | More code | Partial use |
| Firebase Auth | Easy setup | External dependency | ❌ Rejected |

### Key Dependencies:
```
# Backend (requirements.txt)
passlib[bcrypt]>=1.7.4
python-jose[cryptography]>=3.3.0

# Frontend (package.json)
better-auth: ^1.0.0
```

---

## 2. Roman Urdu Translation Strategy

### Decision: Use OpenAI GPT-4 with specialized prompt

### Rationale:
- Roman Urdu is Urdu written in Latin/English alphabet
- OpenAI models understand Roman Urdu well
- Technical terms should remain in English for clarity

### Translation Prompt Template:
```
You are a translator specializing in Roman Urdu (Urdu written in Latin script).

Translate the following technical content to Roman Urdu while:
1. Keeping ALL technical terms in English (e.g., ROS 2, NVIDIA Isaac, Python, API, etc.)
2. Using simple, conversational Roman Urdu
3. Maintaining the same formatting (headings, lists, code blocks)
4. Preserving any code examples without translation

Technical terms to keep in English:
- All programming terms (Python, JavaScript, API, etc.)
- All robotics terms (ROS, URDF, SLAM, LiDAR, etc.)
- All brand names (NVIDIA, Intel, OpenAI, etc.)
- All acronyms (AI, ML, GPU, CPU, etc.)

Content to translate:
{content}
```

### Example Translation:
**English**: "ROS 2 is the Robot Operating System that provides middleware for robot control."
**Roman Urdu**: "ROS 2 aik Robot Operating System hai jo robots ko control karne ke liye middleware provide karta hai."

### Alternatives Considered:
| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| OpenAI GPT-4 | High quality, understands context | Cost | ✅ Selected |
| Google Translate API | Free tier available | Poor Roman Urdu | ❌ Rejected |
| Custom model | Full control | Training required | ❌ Rejected |

---

## 3. Content Personalization Strategy

### Decision: Profile-based prompt engineering

### Rationale:
- User profiles contain experience levels
- Use these levels to adjust content complexity
- Generate personalized explanations on-demand

### Personalization Levels:

| Profile Attribute | Level | Content Adjustment |
|-------------------|-------|-------------------|
| Software Experience | Beginner | Add coding basics, explain syntax |
| Software Experience | Intermediate | Standard explanations |
| Software Experience | Expert | Skip basics, focus on advanced concepts |
| Hardware Experience | None | Add electronics fundamentals |
| Hardware Experience | Arduino/RPi | Reference familiar platforms |
| Hardware Experience | Jetson/Industrial | Use professional terminology |

### Personalization Prompt Template:
```
You are an expert technical writer for a Physical AI & Humanoid Robotics textbook.

Rewrite the following content for a reader with this background:
- Software Experience: {software_exp}
- Hardware Experience: {hardware_exp}
- Robotics Background: {robotics_bg}
- Known Languages: {languages}

Guidelines:
- For BEGINNERS: Add foundational explanations, use analogies, define terms
- For INTERMEDIATE: Provide standard explanations with some context
- For EXPERTS: Be concise, skip basics, focus on advanced concepts

Maintain the same structure but adjust complexity appropriately.

Original Content:
{content}
```

---

## 4. Caching Strategy

### Decision: Cache personalized/translated content in Neon Postgres

### Rationale:
- Avoid repeated API calls for same content
- Reduce latency for returning users
- Lower OpenAI API costs

### Cache Table Design:
```sql
CREATE TABLE content_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),  -- NULL for translations (public)
    chapter_id VARCHAR(255) NOT NULL,
    content_type VARCHAR(50) NOT NULL,  -- 'personalized' or 'translated'
    language VARCHAR(20) DEFAULT 'en',  -- 'en' or 'roman_urdu'
    original_hash VARCHAR(64) NOT NULL, -- MD5 of original content
    cached_content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() + INTERVAL '7 days',

    UNIQUE(user_id, chapter_id, content_type, language)
);
```

### Cache Invalidation:
- Personalized content: When user updates profile
- Translated content: When original chapter content changes
- TTL: 7 days for all cached content

---

## 5. Claude Code Subagents Structure

### Decision: Create 4 specialized subagents in `.claude/agents/`

### Subagent Definitions:

#### 5.1 content-writer.md
- **Purpose**: Generate chapter content following textbook style
- **Triggers**: When creating new chapters or sections
- **Tools**: Read, Write, Glob

#### 5.2 librarian.md
- **Purpose**: Ingest book content into RAG knowledge base
- **Triggers**: When new content is added
- **Tools**: Read, Bash (for ingest.py)

#### 5.3 translator.md
- **Purpose**: Translate content to Roman Urdu
- **Triggers**: When translation is requested
- **Tools**: Read, Write, WebFetch (for API)

#### 5.4 publisher.md
- **Purpose**: Build and deploy Docusaurus site
- **Triggers**: When deployment is requested
- **Tools**: Bash (npm commands), Git operations

---

## 6. Session Management

### Decision: JWT tokens stored in HTTP-only cookies + sessions in DB

### Rationale:
- HTTP-only cookies prevent XSS attacks
- DB sessions allow server-side validation
- Supports logout/session revocation

### Token Structure:
```python
{
    "sub": "user_id",
    "email": "user@example.com",
    "exp": "expiration_timestamp",
    "iat": "issued_at_timestamp"
}
```

### Session Flow:
1. User logs in → Generate JWT → Store session in DB → Set HTTP-only cookie
2. Request comes in → Validate JWT → Check session in DB → Allow/Deny
3. User logs out → Delete session from DB → Clear cookie

---

## Summary of Resolved Clarifications

| Unknown | Resolution |
|---------|------------|
| Better-Auth Python SDK? | Use client-side only + custom FastAPI backend |
| Roman Urdu translation method? | OpenAI GPT-4 with specialized prompt |
| Personalization approach? | Profile-based prompt engineering |
| Caching strategy? | Neon Postgres with 7-day TTL |
| Session management? | JWT + DB sessions + HTTP-only cookies |

---

## Next: Phase 1 Artifacts

With research complete, proceed to create:
1. `data-model.md` - Database schema
2. `contracts/` - API specifications
3. `quickstart.md` - Development setup guide
