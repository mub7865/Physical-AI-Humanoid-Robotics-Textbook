---
id: 0006
title: Prioritize Local Chatbot Fix Before Deploy
stage: frontend-backend-sync-fix
date_iso: 2025-12-04
surface: agent
model: claude-sonnet-4-5-20251101
feature: frontend-backend-sync-fix
branch: main
user: user
command: None
labels: ["chatbot", "local-test", "backend", "frontend"]
links:
  spec: specs/issues/docusaurus-rag-issues.spec.md
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - history/prompts/general/0006-prioritize-local-chatbot-fix.general.prompt.md
tests_yaml: |
  - None
prompt_text: |
  yaar sab se phele sare port band karo or build and deploy karne se phele local mein check karo ke "Error contacting bot. Please try again." chatbot per message karne per ye error na aaye iska sara plan spec task @specs/issues/ mein mujood hai
response_text: |
  Acknowledged user's instruction to first stop all running processes, then locally test the chatbot to ensure the "Error contacting bot" message is resolved before proceeding with build and deploy. Confirmed that spec, plan, and tasks are located in `specs/issues/`.
---
