# Task Checklist: Smart Chat Widget Integration

Based on the feature specification and implementation plan, the following tasks need to be completed for the "Smart Chat Widget Integration" feature.

## Frontend Tasks

1.  [ ] **Component: Create `book/src/theme/ChatWidget.tsx` (UI + Logic)**
    -   Create the basic React functional component file.
    -   Implement the floating action button (FAB) with toggle functionality.
    -   Design the chat window layout with message history display areas, input field, and send button.
    -   Integrate `useState` hooks for `isOpen` (chat window visibility), `messages` (chat history), `inputValue` (current message input), `isLoading` (API call status), and `selectedContext` (highlighted text).
    -   Implement `useEffect` to attach/detach `mouseup` event listener to `window` for capturing selected text.
    -   Add logic to display a "Context found" badge when `selectedContext` is not empty.

2.  [ ] **Styling: Add CSS for the floating bubble and chat window**
    -   Apply minimal, non-conflicting CSS for the FAB (fixed position, z-index).
    -   Style the chat window (fixed position, dimensions, scrollable message area).
    -   Style message bubbles to differentiate user and bot messages.
    -   Ensure styles are scoped or carefully chosen to avoid Docusaurus theme conflicts.

3.  [ ] **Integration: Import and use `<ChatWidget />` in the Docusaurus Layout/Root**
    -   Locate `book/src/theme/Layout.tsx` (or an equivalent global layout component).
    -   Import the `ChatWidget` component.
    -   Render the `<ChatWidget />` component within the main layout to ensure it appears on all pages.

## Backend Tasks (CORS Configuration)

4.  [ ] **Backend: Update `backend/main.py` to enable CORS for `localhost:3000`**
    -   Modify the FastAPI application in `backend/main.py` to include `CORSMiddleware`.
    -   Configure `allow_origins` to include `"http://localhost:3000"` (or the Docusaurus development server URL).
    -   Ensure `allow_methods` and `allow_headers` are appropriately set for `POST` requests.

## Verification Tasks

5.  [ ] **Verify: Test chat functionality and text selection**
    -   Start both the Docusaurus frontend and the FastAPI backend.
    -   Open the Docusaurus book in a browser.
    -   Verify the FAB is visible and toggles the chat window.
    -   Send messages and confirm bot replies are displayed.
    -   Select text on a page, open the chat, and confirm the "Context found" badge appears.
    -   Send a message with selected text and verify the `selected_context` is sent in the network payload (using browser developer tools).
    -   Test with no text selected to ensure `selected_context` is null/empty.
    -   Test error handling by temporarily stopping the backend or simulating an error.
