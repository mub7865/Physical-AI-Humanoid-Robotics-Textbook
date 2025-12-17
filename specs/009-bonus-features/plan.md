# Implementation Plan: Hackathon Bonus Features

**Branch**: `009-bonus-features` | **Date**: 2025-12-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/009-bonus-features/spec.md`

---

## Summary

Implement 4 bonus features for the Physical AI & Humanoid Robotics textbook hackathon:
1. **Better-Auth Authentication** - User signup/signin with background questions (+50 points)
2. **Claude Code Subagents & Skills** - Reusable intelligence for book project (+50 points)
3. **Content Personalization** - Personalize chapter content based on user background (+50 points)
4. **Roman Urdu Translation** - Translate chapters to Roman Urdu on demand (+50 points)

**Technical Approach**: Extend existing FastAPI backend with Better-Auth integration, add new API endpoints for personalization/translation, and create React components for the Docusaurus frontend. Use OpenAI API for AI-powered personalization and Roman Urdu translation.

---

## Technical Context

**Language/Version**: Python 3.10+ (Backend), TypeScript/React (Frontend)
**Primary Dependencies**:
- Backend: FastAPI, Better-Auth (Python SDK), OpenAI SDK, psycopg2
- Frontend: Docusaurus 3.9, React 19, Better-Auth (React SDK)
**Storage**: Neon Serverless Postgres (users, profiles, sessions, cached content)
**Testing**: pytest (Backend), manual testing (Frontend)
**Target Platform**: Web (GitHub Pages + Vercel/Render backend)
**Project Type**: Web application (frontend + backend)
**Performance Goals**:
- Login: <5 seconds
- Personalization: <15 seconds
- Translation: <20 seconds
**Constraints**:
- OpenAI API rate limits
- Vercel serverless function timeout (10s default, 60s max)
**Scale/Scope**: 50+ concurrent users, 8 chapters for personalization/translation

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Zero Vibe Coding | ✅ PASS | spec.md exists, plan.md being created |
| Mandatory Tech Stack | ✅ PASS | Using Docusaurus, FastAPI, Neon Postgres, OpenAI |
| Better-Auth for Auth | ✅ PASS | Explicitly required in constitution |
| RAG & API Contract | ✅ PASS | Extending existing /chat API pattern |
| Content Standards | ✅ PASS | AI-generated personalization follows guidelines |

**Gate Result**: ✅ ALL GATES PASS - Proceed to Phase 0

---

## Project Structure

### Documentation (this feature)

```text
specs/009-bonus-features/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (API specs)
│   ├── auth-api.md
│   ├── personalize-api.md
│   └── translate-api.md
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── main.py                    # FastAPI app (extend)
├── database.py                # Neon DB functions (extend)
├── auth/                      # NEW: Better-Auth integration
│   ├── __init__.py
│   ├── routes.py              # Auth endpoints
│   ├── models.py              # User, Session models
│   └── better_auth.py         # Better-Auth config
├── services/                  # NEW: Business logic
│   ├── __init__.py
│   ├── personalization.py     # Personalize content
│   └── translation.py         # Roman Urdu translation
├── agents/                    # Existing agents (extend)
│   ├── conversation_agent.py
│   └── rag_agent.py
└── requirements.txt           # Add better-auth

book/
├── src/
│   ├── components/            # NEW: Auth & Chapter components
│   │   ├── Auth/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── SignupForm.tsx
│   │   │   └── BackgroundQuestionnaire.tsx
│   │   └── Chapter/
│   │       ├── PersonalizeButton.tsx
│   │       └── TranslateButton.tsx
│   ├── context/               # NEW: Auth context
│   │   └── AuthContext.tsx
│   ├── pages/                 # NEW: Auth pages
│   │   ├── login.tsx
│   │   └── signup.tsx
│   └── theme/
│       ├── Layout/index.tsx   # Extend with AuthProvider
│       └── DocItem/           # NEW: Wrap chapters with buttons
│           └── index.tsx
└── package.json               # Add better-auth client

.claude/
├── agents/                    # NEW: Claude Code subagents
│   ├── content-writer.md
│   ├── librarian.md
│   ├── translator.md
│   └── publisher.md
└── skills/                    # Existing skills (document)
    └── (existing)
```

**Structure Decision**: Web application with existing backend/book structure. Extend rather than replace.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Docusaurus + React)                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────────┐    │
│  │ Login Page  │  │ Signup Page │  │ Background Questionnaire │    │
│  └──────┬──────┘  └──────┬──────┘  └────────────┬─────────────┘    │
│         │                │                      │                   │
│         └────────────────┴──────────────────────┘                   │
│                          │                                          │
│                    AuthContext                                      │
│                          │                                          │
│  ┌───────────────────────┴───────────────────────┐                 │
│  │              Chapter Page                      │                 │
│  │  ┌──────────────────┐  ┌───────────────────┐  │                 │
│  │  │ Personalize Btn  │  │ Roman Urdu Btn    │  │                 │
│  │  └────────┬─────────┘  └─────────┬─────────┘  │                 │
│  └───────────┼──────────────────────┼────────────┘                 │
│              │                      │                               │
└──────────────┼──────────────────────┼───────────────────────────────┘
               │                      │
               ▼                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │
│  │ /auth/signup    │  │ /api/personalize│  │ /api/translate  │     │
│  │ /auth/signin    │  │                 │  │                 │     │
│  │ /auth/signout   │  │                 │  │                 │     │
│  │ /api/profile    │  │                 │  │                 │     │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘     │
│           │                    │                    │               │
│           ▼                    ▼                    ▼               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    OpenAI API                                │   │
│  │  (Personalization Prompts + Roman Urdu Translation)          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    NEON POSTGRES                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐  ┌──────────────────┐  ┌─────────────────────┐   │
│  │    users     │  │   user_profiles  │  │ personalized_cache  │   │
│  │  - id        │  │  - user_id (FK)  │  │  - user_id (FK)     │   │
│  │  - email     │  │  - software_exp  │  │  - chapter_id       │   │
│  │  - password  │  │  - hardware_exp  │  │  - content          │   │
│  │  - created_at│  │  - robotics_bg   │  │  - language         │   │
│  └──────────────┘  │  - languages[]   │  │  - created_at       │   │
│                    │  - goals         │  └─────────────────────┘   │
│  ┌──────────────┐  └──────────────────┘                            │
│  │   sessions   │                                                   │
│  │  - id        │  ┌──────────────────┐                            │
│  │  - user_id   │  │   chat_history   │  (existing)                │
│  │  - token     │  │                  │                            │
│  │  - expires_at│  └──────────────────┘                            │
│  └──────────────┘                                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Implementation Phases

### Phase 1: Authentication Foundation (Better-Auth)
**Priority**: P1 (Required for personalization)
**Dependencies**: None

| Task | Description |
|------|-------------|
| 1.1 | Install Better-Auth Python SDK |
| 1.2 | Create users table in Neon |
| 1.3 | Create sessions table in Neon |
| 1.4 | Implement auth routes (signup, signin, signout) |
| 1.5 | Create user_profiles table |
| 1.6 | Implement profile API endpoint |

### Phase 2: Frontend Authentication
**Priority**: P1
**Dependencies**: Phase 1

| Task | Description |
|------|-------------|
| 2.1 | Install Better-Auth React SDK |
| 2.2 | Create AuthContext provider |
| 2.3 | Create LoginForm component |
| 2.4 | Create SignupForm component |
| 2.5 | Create BackgroundQuestionnaire component |
| 2.6 | Add login/signup pages |
| 2.7 | Wrap Layout with AuthProvider |
| 2.8 | Add auth UI to navbar |

### Phase 3: Content Personalization
**Priority**: P2
**Dependencies**: Phase 1, Phase 2

| Task | Description |
|------|-------------|
| 3.1 | Create personalization service |
| 3.2 | Create /api/personalize endpoint |
| 3.3 | Create PersonalizeButton component |
| 3.4 | Create DocItem wrapper for chapters |
| 3.5 | Implement personalization caching |
| 3.6 | Add "Revert to Original" functionality |

### Phase 4: Roman Urdu Translation
**Priority**: P2
**Dependencies**: Phase 1 (partial - translation works for guests too)

| Task | Description |
|------|-------------|
| 4.1 | Create translation service |
| 4.2 | Create /api/translate endpoint |
| 4.3 | Create TranslateButton component |
| 4.4 | Implement language toggle (English/Roman Urdu) |
| 4.5 | Add technical term preservation logic |

### Phase 5: Claude Code Subagents & Skills
**Priority**: P3
**Dependencies**: None (can be done in parallel)

| Task | Description |
|------|-------------|
| 5.1 | Create content-writer.md subagent |
| 5.2 | Create librarian.md subagent |
| 5.3 | Create translator.md subagent |
| 5.4 | Create publisher.md subagent |
| 5.5 | Document usage instructions |

---

## API Endpoints Summary

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/auth/signup` | POST | No | Create new user account |
| `/auth/signin` | POST | No | Login user |
| `/auth/signout` | POST | Yes | Logout user |
| `/auth/me` | GET | Yes | Get current user info |
| `/api/profile` | GET | Yes | Get user profile |
| `/api/profile` | PUT | Yes | Update user profile |
| `/api/personalize` | POST | Yes | Personalize chapter content |
| `/api/translate` | POST | No | Translate to Roman Urdu |

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Better-Auth compatibility with FastAPI | High | Research alternatives (custom JWT if needed) |
| OpenAI API latency for personalization | Medium | Implement caching, show loading states |
| Roman Urdu translation quality | Medium | Use specific prompts, preserve technical terms |
| Vercel timeout for long operations | Medium | Chunk processing, streaming responses |

---

## Complexity Tracking

> No constitution violations requiring justification. All features align with mandatory tech stack.

---

## Next Steps

1. Run `/sp.tasks` to generate detailed task list
2. Implement Phase 1 (Authentication) first
3. Test authentication before proceeding to personalization
4. Claude Code Subagents can be done in parallel
