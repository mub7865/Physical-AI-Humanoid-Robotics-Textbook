# Template Spec: Embed ChatKit Floating Widget

## Goal

Add a reusable floating ChatKit widget to the app using the `openai-chatkit-frontend-skill`.

## Fill these placeholders

- App framework: `{{framework}}` (e.g. `next-app-router`)
- Widget component path: `{{widget_component_path}}` (e.g. `src/components/ChatKitWidget.tsx`)
- Root layout path: `{{root_layout_path}}` (e.g. `src/app/layout.tsx`)
- Session API route: `{{session_api_route}}` (e.g. `/api/create-session`)

## Requirements

- Create a `ChatKitWidget` component in `{{widget_component_path}}` that:
  - Uses `useChatKit` and `<ChatKit />`.
  - Uses a `getClientSecret` callback pointing to `{{session_api_route}}`. [web:29][web:35][web:49]
  - Renders a toggle button + panel.

- Mount the widget in `{{root_layout_path}}` and:
  - Load the ChatKit script from the official CDN.
  - Ensure it appears on all pages (unless spec says otherwise). [web:35][web:52]

- Keep styling and text configurable by spec:
  - Button position / color.
  - Greeting text and starter prompts.
