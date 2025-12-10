# OpenAI ChatKit Frontend Skill

## Purpose

This skill encodes reusable intelligence for integrating **OpenAI ChatKit** into web frontends (primarily Next.js/React):
- Embedding the ChatKit UI (floating widget or full-page chat).
- Connecting to an Agent Builder workflow via session endpoint. [web:29][web:49]
- Using the recommended `getClientSecret` pattern instead of fully proxying all ChatKit traffic. [web:35]

It should work across projects by only changing:
- The route paths (e.g. `/api/create-session`).
- The workflow id and API key (via env vars).
- Layout / styling choices.

## What this skill must know

- Two main integration styles:

  1. **Starter app style**
     - ChatKit React hook / component (e.g. `useChatKit`, `<ChatKit />`). [web:29][web:35][web:48]
     - Session endpoint like `app/api/create-session/route.ts` that returns a `client_secret`. [web:29][web:49]

  2. **Script embed style**
     - Loading ChatKit JS via `<Script src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js" />`. [web:35][web:52]
     - Using ChatKit web components in layout.

- How to structure a **floating chat widget**:
  - A toggle button (bottom-right).
  - A panel containing the ChatKit component.
  - Global include in root layout so chat is available everywhere. [web:35]

- How to call a **session endpoint** from the frontend:
  - `getClientSecret` callback that POSTs to `/api/create-session` and returns `client_secret`. [web:35][web:49]

## Guardrails

When driven by a spec, this skill should ensure Claude:

- Does NOT:
  - Hardcode workflow id or API key in source code.
  - Rewrite existing app layout from scratch.
  - Add multiple conflicting ChatKit integrations.

- DOES:
  - Use environment variables (e.g. `NEXT_PUBLIC_CHATKIT_WORKFLOW_ID`, `OPENAI_API_KEY`). [web:29][web:49]
  - Keep ChatKit UI in isolated components (e.g. `ChatKitWidget.tsx`).
  - Keep backend session endpoint small and focused on auth only (using `getClientSecret` pattern). [web:35]

## Reusability

The patterns in `examples/` and `templates/` should be reusable for:

- Any Next.js 13+/15 app using the App Router.
- Regular React SPA with a small adjustment for routing.
- Both floating widget and full-page chat screens.

Specs only need to provide:
- Frontend framework (Next.js/React).
- Where global layout/root component lives.
- Desired route for session endpoint.
- Agent Builder workflow id (or env var name holding it). [web:29][web:49]
