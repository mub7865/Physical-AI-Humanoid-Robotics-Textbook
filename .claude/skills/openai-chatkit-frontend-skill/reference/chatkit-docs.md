# ChatKit – Key Docs and Patterns

Use these for grounding and patterns. [web:29][web:49][web:35]

- Official ChatKit guide:
  - https://platform.openai.com/docs/guides/chatkit
- Starter app:
  - https://github.com/openai/openai-chatkit-starter-app
- ChatKit JS / React:
  - https://github.com/openai/chatkit-js
- Advanced integration docs:
  - https://platform.openai.com/docs/guides/custom-chatkit

Key patterns to follow:

- Prefer `getClientSecret` for most apps:
  - Your backend only creates sessions.
  - OpenAI handles threads, messages, streaming. [web:35][web:49]

- Use React hook + component (`useChatKit`, `<ChatKit />`) for:
  - Floating widgets.
  - Standalone pages. [web:35][web:48]

- Load ChatKit script once in your root layout when needed. [web:29][web:35]

This skill assumes we always:
- Keep ChatKit config in one place (e.g. `lib/chatkit-config.ts`).
- Reuse the same session endpoint across widgets/pages.
