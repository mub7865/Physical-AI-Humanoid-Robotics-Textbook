# Feature Specification: Smart Chat Widget Integration

## 1. Introduction
This document outlines the requirements for integrating a "Smart Chat Widget" into the Docusaurus book. The widget will allow users to interact with a backend AI service, providing context from selected text on the page.

## 2. Goals
- Create a reusable React component for the chat widget.
- Implement a floating action button (FAB) for chat access.
- Display a chat window with message history.
- Capture user-selected text as context for backend API calls.
- Integrate with the backend API at `http://localhost:8000/chat`.
- Ensure the widget is globally available on all book pages.

## 3. Requirements

### 3.1. Component Creation
- **REQ-FE-001:** Create a new React functional component file at `book/src/theme/ChatWidget.tsx`.

### 3.2. User Interface (UI) Design
- **REQ-FE-002:** The widget must include a floating action button (FAB) positioned at the bottom-right corner of the screen. The button should display a chat icon (e.g., 💬).
- **REQ-FE-003:** Clicking the FAB must toggle the visibility of a chat window.
- **REQ-FE-004:** The chat window must display message history, distinguishing between user input and bot responses (e.g., using different bubble styles or alignments).
- **REQ-FE-005:** The chat window must include an input field for user messages and a send button.

### 3.3. Selected Text Logic (Critical)
- **REQ-FE-006:** The component must detect if the user has highlighted any text on the page using `window.getSelection()`.
- **REQ-FE-007:** If text is selected, a "Context found" badge or similar indicator must be displayed prominently within the chat window.
- **REQ-FE-008:** The selected text must be sent to the backend API as part of the message payload, specifically in a field named `selected_context`. If no text is selected, `selected_context` should be null or an empty string.

### 3.4. API Integration
- **REQ-FE-009:** Implement a `sendMessage(text)` function within the component that sends a `POST` request to `http://localhost:8000/chat`.
- **REQ-FE-010:** The `POST` request body must include the user's message and the `selected_context` (if available).
- **REQ-FE-011:** The UI must display a "Thinking..." or similar loading indicator while awaiting a response from the backend API.
- **REQ-FE-012:** Handle successful API responses by displaying the bot's reply in the chat history.
- **REQ-FE-013:** Implement basic error handling for API failures (e.g., displaying an error message to the user).

### 3.5. Global Integration
- **REQ-FE-014:** The `ChatWidget.tsx` component must be integrated such that it appears on every page of the Docusaurus book. This will likely involve importing it into a core Docusaurus layout component (e.g., `Layout` or `Root`).

## 4. Constraints
- **CON-FE-001:** Use React functional components.
- **CON-FE-002:** Utilize React hooks (`useState`, `useEffect`) for state management and lifecycle events.
- **CON-FE-003:** Ensure the component's CSS styling does not conflict with or break the existing Docusaurus theme.

## 5. Non-Functional Requirements (NFRs)
- **NFR-FE-001 - Performance:** The widget should load efficiently and not significantly impact page load times.
- **NFR-FE-002 - Responsiveness:** The UI should be responsive across different screen sizes (desktop, tablet, mobile).
- **NFR-FE-003 - Accessibility:** Basic accessibility considerations should be applied (e.g., keyboard navigation for the chat input).

## 6. Open Questions
- What specific chat icon should be used for the FAB?
- Are there any specific styling guidelines (colors, fonts, sizes) to adhere to beyond not breaking the Docusaurus theme?
- How should API errors be presented to the user (e.g., a simple "Error contacting bot" or more detailed messages)?
