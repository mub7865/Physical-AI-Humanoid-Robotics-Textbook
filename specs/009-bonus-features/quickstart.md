# Quickstart Guide: Bonus Features Development

**Feature**: 009-bonus-features
**Date**: 2025-12-17

---

## Prerequisites

Before starting, ensure you have:

- [x] Node.js 20+ installed
- [x] Python 3.10+ installed
- [x] Git configured
- [x] Access to Neon Postgres database
- [x] OpenAI API key

---

## 1. Backend Setup

### 1.1 Install New Dependencies

```bash
cd backend

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate   # Windows

# Install new packages
pip install passlib[bcrypt] python-jose[cryptography]

# Update requirements.txt
pip freeze > requirements.txt
```

### 1.2 Environment Variables

Add to `backend/.env`:

```env
# Existing
OPENAI_API_KEY=sk-...
QDRANT_URL=https://...
QDRANT_API_KEY=...
NEON_DB_URL=postgresql://...

# NEW: Auth Configuration
JWT_SECRET_KEY=your-super-secret-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRE_DAYS=7

# NEW: Better-Auth (optional, for client config)
BETTER_AUTH_URL=http://localhost:8000
```

### 1.3 Database Migration

Run the migration script to create new tables:

```bash
# Connect to Neon and run migration
psql $NEON_DB_URL -f specs/009-bonus-features/migration.sql
```

Or manually in Neon console:

```sql
-- Copy content from data-model.md Migration Script section
```

### 1.4 Create Auth Module

```bash
mkdir -p backend/auth
touch backend/auth/__init__.py
touch backend/auth/routes.py
touch backend/auth/models.py
touch backend/auth/utils.py
```

### 1.5 Create Services Module

```bash
mkdir -p backend/services
touch backend/services/__init__.py
touch backend/services/personalization.py
touch backend/services/translation.py
```

---

## 2. Frontend Setup

### 2.1 Install New Dependencies

```bash
cd book

# Install Better-Auth client
npm install better-auth

# Install additional UI dependencies (if needed)
npm install @headlessui/react  # For modals/dialogs
```

### 2.2 Create Component Directories

```bash
mkdir -p src/components/Auth
mkdir -p src/components/Chapter
mkdir -p src/context
```

### 2.3 Environment Variables

Create `book/.env`:

```env
VITE_API_URL=http://localhost:8000
VITE_BETTER_AUTH_URL=http://localhost:8000
```

For production (`book/.env.production`):

```env
VITE_API_URL=https://your-backend.vercel.app
VITE_BETTER_AUTH_URL=https://your-backend.vercel.app
```

---

## 3. Development Workflow

### 3.1 Start Backend

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### 3.2 Start Frontend

```bash
cd book
npm start
```

### 3.3 Test Authentication Flow

1. Open http://localhost:3000
2. Click "Sign Up"
3. Fill email/password
4. Complete background questions
5. Verify profile saved in Neon

### 3.4 Test Personalization

1. Login with test account
2. Navigate to any chapter
3. Click "Personalize Content"
4. Verify content adapts to profile

### 3.5 Test Translation

1. Navigate to any chapter
2. Click "Roman Urdu"
3. Verify content translated
4. Technical terms should remain English

---

## 4. Claude Code Subagents Setup

### 4.1 Create Agent Definitions

```bash
mkdir -p .claude/agents
```

Create the following files:
- `.claude/agents/content-writer.md`
- `.claude/agents/librarian.md`
- `.claude/agents/translator.md`
- `.claude/agents/publisher.md`

### 4.2 Example Agent Definition

`.claude/agents/translator.md`:
```markdown
# Agent: Roman Urdu Translator

## Purpose
Translate book content to Roman Urdu while preserving technical terms.

## Tools
- Read: Read chapter content
- Write: Write translated content
- WebFetch: Call translation API

## Instructions
1. Read the chapter file
2. Send content to /api/translate endpoint
3. Save translated content to parallel file

## Usage
"Translate chapter-2-ros2 to Roman Urdu"
```

---

## 5. File Structure After Setup

```
backend/
├── main.py                 # Updated with auth routes
├── database.py             # Updated with new tables
├── auth/
│   ├── __init__.py
│   ├── routes.py           # Auth endpoints
│   ├── models.py           # Pydantic models
│   └── utils.py            # JWT helpers
├── services/
│   ├── __init__.py
│   ├── personalization.py  # Personalize logic
│   └── translation.py      # Translation logic
└── requirements.txt        # Updated

book/
├── src/
│   ├── components/
│   │   ├── Auth/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── SignupForm.tsx
│   │   │   └── BackgroundQuestionnaire.tsx
│   │   └── Chapter/
│   │       ├── PersonalizeButton.tsx
│   │       └── TranslateButton.tsx
│   ├── context/
│   │   └── AuthContext.tsx
│   └── theme/
│       └── DocItem/
│           └── index.tsx
└── package.json            # Updated

.claude/
└── agents/
    ├── content-writer.md
    ├── librarian.md
    ├── translator.md
    └── publisher.md
```

---

## 6. Testing Checklist

### Authentication
- [ ] User can sign up with email/password
- [ ] User sees background questions after signup
- [ ] User can login with credentials
- [ ] Session persists across page refresh
- [ ] User can logout

### Profile
- [ ] Profile is created after questions
- [ ] Profile can be updated
- [ ] Profile data shows in settings

### Personalization
- [ ] Button shows only for logged-in users
- [ ] Content personalizes based on profile
- [ ] Cached content loads faster
- [ ] "Revert" returns original content

### Translation
- [ ] Button shows for all users
- [ ] Content translates to Roman Urdu
- [ ] Technical terms stay in English
- [ ] Code blocks remain untouched
- [ ] Toggle returns to English

### Subagents
- [ ] content-writer invocable
- [ ] librarian invocable
- [ ] translator invocable
- [ ] publisher invocable

---

## 7. Common Issues & Solutions

### Issue: JWT Token Invalid
```
Solution: Check JWT_SECRET_KEY is at least 32 characters
```

### Issue: CORS Error
```
Solution: Ensure backend CORS allows frontend origin
```

### Issue: Profile Not Found
```
Solution: Complete signup flow including background questions
```

### Issue: Translation Too Slow
```
Solution: Check OpenAI API key, consider caching
```

### Issue: Personalization Not Working
```
Solution: Verify user profile exists, check API logs
```

---

## 8. Next Steps

After setup is complete:

1. Run `/sp.tasks` to generate detailed task list
2. Start with Phase 1 (Authentication)
3. Test each phase before proceeding
4. Document any issues encountered
