# Template Spec: Wire ChatKit Session Endpoint

## Goal

Create a minimal backend endpoint that returns a ChatKit `client_secret` for a given workflow.

## Fill these placeholders

- Session route file: `{{session_route_file}}`
  - e.g. Next.js: `src/app/api/create-session/route.ts`
- Env vars:
  - `{{env_api_key_name}}` (e.g. `OPENAI_API_KEY`)
  - `{{env_workflow_id_name}}` (e.g. `NEXT_PUBLIC_CHATKIT_WORKFLOW_ID`)

## Requirements

- Implement a POST handler in `{{session_route_file}}` that:
  - Reads the API key and workflow id from env vars.
  - Calls the ChatKit/Agent Builder session API (as in starter app). [web:29][web:49][web:50]
  - Returns JSON `{ "client_secret": "..." }`.

- Follow the **recommended `getClientSecret` pattern**:
  - Endpoint handles only auth/session creation.
  - ChatKit talks directly to OpenAI for threads/messages. [web:35][web:49]

- Do NOT:
  - Log secrets.
  - Hardcode workflow ids or keys.
