---
id: 001
title: Docusaurus Deployment and RAG Chatbot Issues
stage: spec
date_iso: 2025-12-04
surface: agent
model: claude-sonnet-4-5-20251101
feature: docusaurus-rag-fix
branch: main
user: user
command: None
labels: ["deployment", "frontend", "backend", "rag", "qdrant"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - specs/issues/docusaurus-rag-issues.spec.md
tests_yaml: |
  - None
prompt_text: |
  (Implicit from user's request to create a spec for the identified issues)
response_text: |
  Created the initial spec file for Docusaurus deployment and RAG chatbot issues.
---
# Spec: Docusaurus Deployment and RAG Chatbot Issues

## 1. Problem Description

This document outlines the specifications for addressing two critical issues identified in the AI-Native Interactive Book project:

### Issue 1: Docusaurus GitHub Pages Deployment Failure

**Problem:** The Docusaurus-based book, when deployed to GitHub Pages, renders as plain HTML without any CSS or JavaScript, resulting in a broken user interface. The site functions correctly when run locally. This indicates a potential misconfiguration in the Docusaurus build process, GitHub Pages settings, or incorrect pathing for assets post-deployment.

**User Impact:** Users cannot properly view or interact with the book content online, severely hindering the primary goal of publishing an interactive textbook.

### Issue 2: RAG Chatbot Backend and Qdrant Ingestion Failure

**Problem:**
a. **Backend Non-functionality:** The integrated Retrieval-Augmented Generation (RAG) chatbot's backend is not responding, consistently returning an "Error contacting bot" message upon interaction. This prevents the chatbot from processing user queries.
b. **Incorrect Qdrant Data Ingestion:** The Qdrant vector database, intended to store only the book's content for RAG, appears to have ingested extraneous data, including UI elements like "Smart Chat..." from the frontend. This dilutes the relevance of retrieval and indicates a flaw in the data ingestion pipeline.

**User Impact:** The core RAG chatbot functionality is non-operational, preventing users from asking questions about the book content. Furthermore, inaccurate retrieval due to malformed data in Qdrant will lead to poor or irrelevant chatbot responses even if the backend issues are resolved.

## 2. Goals

The primary goals are to:
1.  **Resolve Docusaurus Deployment:** Ensure the Docusaurus site deploys correctly to GitHub Pages, with all CSS, JavaScript, and other assets loading as expected, rendering the book fully functional and interactive.
2.  **Restore RAG Chatbot Backend:** Fix all issues preventing the FastAPI backend from communicating with the chatbot frontend and processing queries effectively.
3.  **Correct Qdrant Data Ingestion:** Implement a robust and accurate data ingestion process for Qdrant, ensuring that *only* the book's specific content (e.g., Markdown files from `book/docs/`) is processed and stored, excluding any UI elements or non-content data.

## 3. In Scope

*   **Frontend:**
    *   Reviewing Docusaurus configuration (`docusaurus.config.js`, `package.json`, build scripts) for GitHub Pages compatibility.
    *   Debugging asset loading paths (CSS, JS, images) on GitHub Pages.
    *   Verifying `baseUrl` and `trailingSlash` settings in Docusaurus.
    *   Ensuring correct build output for deployment.
*   **Backend:**
    *   Debugging FastAPI application (e.g., `backend/main.py`) for errors, connectivity, and endpoint functionality.
    *   Checking environment variables and dependencies.
    *   Verifying integration with OpenAI Agents SDK and Qdrant Client.
    *   Testing the `/chat` endpoint.
*   **Data Ingestion (Qdrant):**
    *   Identifying the current ingestion script/logic (e.g., `ingest.py` or `ingest_book_content.py` mentioned in `git status`).
    *   Modifying the ingestion process to strictly target book content (e.g., `book/docs/**/*.md`).
    *   Implementing a verification step post-ingestion to ensure data quality.
    *   Clearing and re-ingesting data into Qdrant after fixes.

## 4. Out of Scope

*   Major refactoring of existing Docusaurus content or structure unless directly required to fix deployment.
*   Implementing new chatbot features beyond basic RAG functionality.
*   Optimization of the RAG model or Qdrant performance beyond fixing incorrect ingestion.
*   Changes to the core book content or its educational modules.
*   Local development environment setup issues (focus is on deployment and backend functionality).

## 5. Acceptance Criteria

### Docusaurus Deployment
*   The deployed Docusaurus site on GitHub Pages loads correctly, displaying all styles, scripts, and interactive elements.
*   No console errors related to failed asset loading are present on the deployed site.
*   Navigation within the deployed book functions as expected.

### RAG Chatbot Backend
*   The chatbot frontend successfully communicates with the backend, receiving valid responses.
*   No "Error contacting bot" or similar messages are displayed when interacting with the chatbot.
*   Backend logs show successful processing of chat queries.

### Qdrant Data Ingestion
*   The Qdrant database contains only text content extracted from the specified book source files (e.g., Markdown files).
*   No UI elements, code snippets (unless part of book content), or other non-book text are found in Qdrant upon inspection.
*   The ingestion process completes without errors.

## 6. High-Level Plan (Initial Thoughts - to be refined in Plan phase)

1.  **Investigate Docusaurus Deployment:**
    *   Review Docusaurus build configuration (`docusaurus.config.js`).
    *   Inspect GitHub Pages repository settings (source, custom domain).
    *   Check browser developer tools for failed network requests on the deployed site.
    *   Potentially use `npm run build` and `serve -s build` locally to verify build output directly.
2.  **Diagnose Backend Errors:**
    *   Check backend server logs for detailed error messages when the chatbot fails.
    *   Verify `requirements.txt` and ensure all dependencies are installed.
    *   Run backend in debug mode to pinpoint exact failure points.
3.  **Rectify Qdrant Ingestion:**
    *   Analyze existing ingestion scripts to understand how data is currently being sourced and processed.
    *   Modify the script to ensure it explicitly targets `book/docs/**/*.md` files (or the correct book content directory).
    *   Add logging to the ingestion process to track what data is being added.
    *   Implement a full clear and re-ingest cycle for Qdrant.

This spec will serve as the foundation for the subsequent planning, task creation, and implementation phases.