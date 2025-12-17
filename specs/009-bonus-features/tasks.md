# Implementation Tasks: Hackathon Bonus Features

**Feature**: 009-bonus-features
**Branch**: `009-bonus-features`
**Generated**: 2025-12-17
**Total Tasks**: 45

---

## Task Summary

| Phase | Description | Tasks | Story |
|-------|-------------|-------|-------|
| 1 | Setup & Dependencies | 6 | - |
| 2 | Foundational (Database) | 5 | - |
| 3 | User Story 1: Registration | 10 | US1 |
| 4 | User Story 2: Login | 6 | US2 |
| 5 | User Story 3: Personalization | 8 | US3 |
| 6 | User Story 4: Translation | 7 | US4 |
| 7 | User Story 5: Subagents | 5 | US5 |
| 8 | Polish & Integration | 3 | - |

---

## Phase 1: Setup & Dependencies

**Goal**: Install all required dependencies and configure project structure.

- [x] T001 Install backend dependencies (passlib, python-jose) in backend/requirements.txt
- [x] T002 [P] Install frontend dependency (better-auth) in book/package.json
- [x] T003 [P] Create backend/auth/ directory structure with __init__.py
- [x] T004 [P] Create backend/services/ directory structure with __init__.py
- [x] T005 [P] Create book/src/components/Auth/ directory structure
- [x] T006 [P] Create book/src/components/Chapter/ directory structure

---

## Phase 2: Foundational (Database Schema)

**Goal**: Create all required database tables in Neon Postgres. MUST complete before user stories.

- [x] T007 Create users table with schema from data-model.md in backend/database.py
- [x] T008 Create user_profiles table with constraints in backend/database.py
- [x] T009 Create sessions table with indexes in backend/database.py
- [x] T010 Create content_cache table for personalization/translation in backend/database.py
- [x] T011 Add user_id column to existing chat_history table in backend/database.py

---

## Phase 3: User Story 1 - New User Registration with Background Profile (P1)

**Story Goal**: A new visitor can create an account and provide their technical background.

**Independent Test**: Complete signup flow → verify user + profile data stored in Neon.

**Acceptance Criteria**:
- Visitor clicks "Sign Up" and sees registration form
- Valid credentials submission prompts background questions
- Profile saved → user logged in automatically
- Duplicate email shows error message

### Backend Tasks

- [x] T012 [US1] Create Pydantic models (UserCreate, UserResponse) in backend/auth/models.py
- [x] T013 [US1] Create password hashing utilities (bcrypt) in backend/auth/utils.py
- [x] T014 [US1] Create JWT token generation utilities in backend/auth/utils.py
- [x] T015 [US1] Implement POST /auth/signup endpoint in backend/auth/routes.py
- [x] T016 [US1] Create UserProfileCreate model in backend/auth/models.py
- [x] T017 [US1] Implement POST /api/profile endpoint in backend/auth/routes.py

### Frontend Tasks

- [x] T018 [P] [US1] Create SignupForm component in book/src/components/Auth/SignupForm.tsx
- [x] T019 [P] [US1] Create BackgroundQuestionnaire component in book/src/components/Auth/BackgroundQuestionnaire.tsx
- [x] T020 [US1] Create signup page in book/src/pages/signup.tsx
- [x] T021 [US1] Register auth routes in backend/main.py

---

## Phase 4: User Story 2 - Returning User Login (P1)

**Story Goal**: A registered user can sign in and maintain session across pages.

**Independent Test**: Login with valid credentials → session persists → logout works.

**Acceptance Criteria**:
- Valid credentials → login + redirect to homepage
- Invalid credentials → generic error message
- Session persists across page navigation
- Logout ends session

### Backend Tasks

- [x] T022 [US2] Create LoginRequest and TokenResponse models in backend/auth/models.py
- [x] T023 [US2] Implement POST /auth/signin endpoint in backend/auth/routes.py
- [x] T024 [US2] Implement POST /auth/signout endpoint in backend/auth/routes.py
- [x] T025 [US2] Implement GET /auth/me endpoint in backend/auth/routes.py

### Frontend Tasks

- [x] T026 [P] [US2] Create LoginForm component in book/src/components/Auth/LoginForm.tsx
- [x] T027 [US2] Create AuthContext provider in book/src/context/AuthContext.tsx
- [x] T028 [US2] Create login page in book/src/pages/login.tsx
- [x] T029 [US2] Wrap Layout with AuthProvider in book/src/theme/Layout/index.tsx
- [ ] T030 [US2] Add auth UI (Login/Logout buttons) to navbar in book/src/theme/Navbar/

---

## Phase 5: User Story 3 - Personalize Chapter Content (P2)

**Story Goal**: Logged-in user can personalize chapter content based on their background.

**Independent Test**: Login → view chapter → click Personalize → content adapts to profile.

**Acceptance Criteria**:
- Personalize button visible only for logged-in users
- Content regenerates based on profile (beginner/intermediate/expert)
- Cached content loads faster on refresh
- Revert to original works

**Dependencies**: Requires US1 (registration) and US2 (login) completed.

### Backend Tasks

- [x] T031 [US3] Create personalization service with OpenAI integration in backend/services/personalization.py
- [x] T032 [US3] Create personalization prompt templates in backend/services/personalization.py
- [x] T033 [US3] Implement POST /api/personalize endpoint in backend/main.py
- [x] T034 [US3] Implement cache lookup/save logic for personalized content in backend/services/personalization.py

### Frontend Tasks

- [x] T035 [P] [US3] Create PersonalizeButton component in book/src/components/Chapter/PersonalizeButton.tsx
- [ ] T036 [US3] Create DocItem wrapper to inject buttons in book/src/theme/DocItem/index.tsx
- [ ] T037 [US3] Add chapter content state management for personalization in book/src/theme/DocItem/index.tsx
- [x] T038 [US3] Implement "Revert to Original" functionality in book/src/components/Chapter/PersonalizeButton.tsx

---

## Phase 6: User Story 4 - Translate to Roman Urdu (P2)

**Story Goal**: Any user can translate chapter content to Roman Urdu.

**Independent Test**: View chapter → click Roman Urdu → content translates → technical terms preserved.

**Acceptance Criteria**:
- Roman Urdu button visible for all users (guests included)
- Content translates with technical terms in English
- Toggle back to English works
- Loading state shows during translation

**Dependencies**: Can start after Phase 2 (database). Does NOT require US1/US2.

### Backend Tasks

- [x] T039 [US4] Create translation service with OpenAI integration in backend/services/translation.py
- [x] T040 [US4] Create translation prompt with technical term preservation in backend/services/translation.py
- [x] T041 [US4] Implement POST /api/translate endpoint in backend/main.py
- [x] T042 [US4] Implement public cache for translations (user_id=NULL) in backend/services/translation.py

### Frontend Tasks

- [x] T043 [P] [US4] Create TranslateButton component in book/src/components/Chapter/TranslateButton.tsx
- [ ] T044 [US4] Add language toggle state in book/src/theme/DocItem/index.tsx
- [x] T045 [US4] Implement loading state and error handling in book/src/components/Chapter/TranslateButton.tsx

---

## Phase 7: User Story 5 - Claude Code Subagents & Skills (P3)

**Story Goal**: Development team has custom Claude Code subagents for book automation.

**Independent Test**: Invoke each subagent → verify expected output.

**Acceptance Criteria**:
- content-writer generates chapter content
- librarian ingests content to RAG
- translator translates content
- publisher deploys site
- All subagents documented

**Dependencies**: None - can be done in parallel with other phases.

- [x] T046 [P] [US5] Create content-writer subagent in .claude/agents/content-writer.md
- [x] T047 [P] [US5] Create librarian subagent in .claude/agents/librarian.md
- [x] T048 [P] [US5] Create translator subagent in .claude/agents/translator.md
- [x] T049 [P] [US5] Create publisher subagent in .claude/agents/publisher.md
- [x] T050 [US5] Document all subagents usage in .claude/agents/README.md

---

## Phase 8: Polish & Cross-Cutting Concerns

**Goal**: Final integration, error handling, and deployment readiness.

- [x] T051 Add CORS configuration for auth endpoints in backend/main.py
- [ ] T052 Add rate limiting for auth and translation endpoints in backend/main.py
- [x] T053 Update environment variables documentation in backend/.env.example

---

## Dependencies Graph

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Database) ─────────────────────────────────┐
    │                                               │
    ├──────────────┬──────────────┐                 │
    ▼              ▼              ▼                 │
Phase 3 (US1)  Phase 6 (US4)  Phase 7 (US5)        │
    │              │              │                 │
    ▼              │              │                 │
Phase 4 (US2)     │              │                 │
    │              │              │                 │
    ▼              │              │                 │
Phase 5 (US3)     │              │                 │
    │              │              │                 │
    └──────────────┴──────────────┘                 │
                   │                                │
                   ▼                                │
              Phase 8 (Polish) ◄────────────────────┘
```

---

## Parallel Execution Opportunities

### Within Phase 1 (Setup)
```
T001 (backend deps) ──┐
T002 (frontend deps) ─┼── All parallel
T003 (auth dir) ──────┤
T004 (services dir) ──┤
T005 (Auth comps) ────┤
T006 (Chapter comps) ─┘
```

### Within Phase 3 (US1 - Registration)
```
T012-T017 (Backend) ─► Sequential
T018, T019 (Frontend components) ─► Parallel with each other
T018, T019 ─► Can start after T015 (signup endpoint)
```

### Cross-Phase Parallelism
```
Phase 6 (US4 - Translation) ─┐
                             ├── Can run in parallel after Phase 2
Phase 7 (US5 - Subagents) ───┘
```

---

## Implementation Strategy

### MVP Scope (Recommended First Delivery)
**User Story 1 + User Story 2** = Authentication working
- Setup (Phase 1)
- Database (Phase 2)
- Registration (Phase 3)
- Login (Phase 4)

**Delivers**: Users can signup, login, and maintain sessions.

### Second Increment
**User Story 3** = Personalization
- Personalization service
- Frontend button

**Delivers**: Logged-in users can personalize content.

### Third Increment
**User Story 4 + User Story 5** = Translation + Subagents (can be parallel)
- Translation service
- Claude Code subagents

**Delivers**: Full bonus feature set.

---

## Task Statistics

| Metric | Count |
|--------|-------|
| **Total Tasks** | 53 |
| **Setup Tasks** | 6 |
| **Database Tasks** | 5 |
| **US1 Tasks** | 10 |
| **US2 Tasks** | 9 |
| **US3 Tasks** | 8 |
| **US4 Tasks** | 7 |
| **US5 Tasks** | 5 |
| **Polish Tasks** | 3 |
| **Parallelizable [P]** | 16 |
| **Backend Tasks** | 25 |
| **Frontend Tasks** | 18 |

---

## File Paths Reference

### Backend Files (New)
```
backend/
├── auth/
│   ├── __init__.py
│   ├── models.py       (T012, T016, T022)
│   ├── routes.py       (T015, T017, T023, T024, T025)
│   └── utils.py        (T013, T014)
├── services/
│   ├── __init__.py
│   ├── personalization.py  (T031, T032, T034)
│   └── translation.py      (T039, T040, T042)
├── database.py         (T007-T011)
├── main.py             (T021, T033, T041, T051, T052)
└── requirements.txt    (T001)
```

### Frontend Files (New)
```
book/src/
├── components/
│   ├── Auth/
│   │   ├── LoginForm.tsx              (T026)
│   │   ├── SignupForm.tsx             (T018)
│   │   └── BackgroundQuestionnaire.tsx (T019)
│   └── Chapter/
│       ├── PersonalizeButton.tsx      (T035, T038)
│       └── TranslateButton.tsx        (T043, T045)
├── context/
│   └── AuthContext.tsx                (T027)
├── pages/
│   ├── login.tsx                      (T028)
│   └── signup.tsx                     (T020)
└── theme/
    ├── Layout/index.tsx               (T029)
    ├── Navbar/                        (T030)
    └── DocItem/index.tsx              (T036, T037, T044)
```

### Claude Code Files (New)
```
.claude/agents/
├── content-writer.md   (T046)
├── librarian.md        (T047)
├── translator.md       (T048)
├── publisher.md        (T049)
└── README.md           (T050)
```
