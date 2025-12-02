# Implementation Plan: Smart Chat Widget Integration

## 1. Scope and Dependencies

### In Scope:
- Creation of `ChatWidget.tsx` React component.
- Implementation of UI elements: Floating Action Button (FAB), chat window, message display, input field, send button.
- Logic for capturing and displaying user-selected text as context.
- Integration with the backend `/chat` API endpoint.
- Global integration of the widget across all Docusaurus book pages.

### Out of Scope:
- Advanced styling or custom theming beyond basic functional UI.
- Complex user authentication within the widget (assumes backend handles session).
- Persistent chat history across user sessions (will reset on page refresh).
- Real-time updates from the backend (will rely on explicit user message sending).

### External Dependencies:
- Backend API: `http://localhost:8000/chat` (owned by backend team/service).
- Docusaurus 3.x framework for global component injection.
- React library for component development.

## 2. Key Decisions and Rationale

### Decision 1: Component Structure and State Management
- **Options Considered:** Class components vs. Functional components with Hooks.
- **Trade-offs:** Class components are more verbose; Hooks provide cleaner state logic and better reusability.
- **Rationale:** Adhering to `CON-FE-001` and `CON-FE-002`, we will use React functional components with `useState` and `useEffect` hooks for managing UI visibility, message history, input values, loading states, and selected text.

### Decision 2: Selected Text Capture Mechanism
- **Options Considered:** Various third-party libraries for text selection vs. native `window.getSelection()`.
- **Trade-offs:** Libraries add bundle size; `window.getSelection()` is native but requires manual event listener management.
- **Rationale:** As per `REQ-FE-006`, we will use `window.getSelection()` within a `useEffect` hook to capture highlighted text on `mouseup` events. This minimizes external dependencies and provides direct control.

### Decision 3: Global Widget Integration
- **Options Considered:** Injecting into `Root.tsx`, `Layout.tsx`, or individual page components.
- **Trade-offs:** `Root.tsx` is often for global providers/context; `Layout.tsx` directly wraps page content; individual pages are too granular.
- **Rationale:** `REQ-FE-014` requires global presence. Injecting the `ChatWidget.tsx` into `book/src/theme/Layout.tsx` is the most robust and standard Docusaurus 3.x approach to ensure it appears on every page without interfering with routing.

### Decision 4: API Communication Method
- **Options Considered:** Axios vs. native `fetch` API.
- **Trade-offs:** Axios offers more features (interceptors, automatic JSON parsing) but adds dependency; `fetch` is native and lightweight.
- **Rationale:** Given the single API endpoint and simple `POST` request, the native `fetch` API will be sufficient (`REQ-FE-009`) to reduce bundle size and external dependencies.

## 3. Interfaces and API Contracts

### Public API (Frontend to Backend):
- **Endpoint:** `POST http://localhost:8000/chat`
- **Request Body (JSON):**
  ```json
  {
    "message": "string",
    "selected_context": "string | null"
  }
  ```
  - `message`: User's input message (string, required).
  - `selected_context`: User-highlighted text (string or null, as per `REQ-FE-008`).
- **Response Body (JSON - expected):
  ```json
  {
    "reply": "string"
  }
  ```
  - `reply`: Bot's response message (string).
- **Error Taxonomy:**
  - HTTP Status 4xx: Client-side errors (e.g., invalid input).
  - HTTP Status 5xx: Server-side errors (e.g., backend issues).
  - Frontend will display a generic error message for any non-2xx response (`REQ-FE-013`).

## 4. Non-Functional Requirements (NFRs) and Budgets

### Performance:
- **NFR-FE-001:** Widget load time should not significantly exceed 200ms on a typical broadband connection.
- Minimal impact on Docusaurus page rendering performance.

### Reliability:
- API calls should have a timeout (default `fetch` timeout is often sufficient, or implement manual abort controller).
- Graceful degradation: If the backend API is unavailable, the chat widget should display an informative error message without crashing the application.

### Security:
- No sensitive user data will be stored client-side persistently.
- Input sanitization will be considered if user input is reflected directly in the UI (though React typically handles XSS for text content).

## 5. Data Management and Migration

- No persistent data storage required on the frontend.
- Chat history will be maintained in component state and will reset on page reload.

## 6. Operational Readiness

### Observability:
- Console logs for debugging API requests/responses and state changes during development.

### Deployment and Rollback:
- Standard Docusaurus build and deployment process (no special considerations for this component).

## 7. Risk Analysis and Mitigation

### Risk 1: CSS Conflicts with Docusaurus Theme
- **Blast Radius:** Broken UI, inconsistent look and feel.
- **Mitigation:** Use scoped CSS (e.g., CSS modules) or apply minimal inline styles/tailwind classes. Thorough testing of widget rendering across various Docusaurus pages and themes (`CON-FE-003`).

### Risk 2: `window.getSelection()` Edge Cases
- **Blast Radius:** Incorrect context sent to the backend, leading to irrelevant bot responses.
- **Mitigation:** Test text selection across different HTML elements (paragraphs, headings, code blocks) and empty selections. Ensure robust trimming and null/empty string handling for `selected_context` (`REQ-FE-008`).

### Risk 3: Backend API Unavailability/Errors
- **Blast Radius:** Poor user experience, perceived as broken feature.
- **Mitigation:** Implement `isLoading` state (`REQ-FE-011`) and basic error display (`REQ-FE-013`). Provide clear feedback to the user if the backend fails to respond or returns an error.

## 8. Evaluation and Validation

### Definition of Done:
- `ChatWidget.tsx` component created and functional (`REQ-FE-001`).
- FAB correctly toggles chat window (`REQ-FE-002`, `REQ-FE-003`).
- Message history displays user/bot messages clearly (`REQ-FE-004`).
- "Context found" badge appears/disappears based on text selection (`REQ-FE-007`).
- `selected_context` is correctly sent to backend (`REQ-FE-008`).
- `sendMessage` function successfully communicates with backend API (`REQ-FE-009`, `REQ-FE-010`).
- Loading states and error handling implemented (`REQ-FE-011`, `REQ-FE-013`).
- Widget appears on all book pages via `Layout.tsx` integration (`REQ-FE-014`).
- Constraints on React functional components, hooks, and CSS compatibility are met (`CON-FE-001`, `CON-FE-002`, `CON-FE-003`).

### Output Validation:
- Manual testing across various Docusaurus pages.
- Browser console checks for errors and network requests.
- Visual inspection for UI consistency and responsiveness.

## 9. Architectural Decision Record (ADR):
- No immediately significant architectural decisions warranting a separate ADR at this stage, as the plan follows standard React/Docusaurus practices and specific user instructions. The integration points are well-defined. However, if the project grows to include more complex frontend architecture (e.g., global state management solutions, design systems), an ADR might be suggested then.