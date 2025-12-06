# Tasks: Resolving Deployment and Backend/RAG Issues

## 1. Frontend Deployment Issue: GitHub Pages CSS/JS Loading Failure

### Task List

1.  **Task: Docusaurus Configuration Review**
    *   **Description:** `docusaurus.config.js` aur `package.json` files ko read kar ke `baseUrl`, `url`, aur deploy script ki mojooda settings ko note karein.
    *   **Acceptance Criteria:**
        *   `docusaurus.config.js` file content read kiya gaya ho.
        *   `package.json` file content read kiya gaya ho.
        *   `baseUrl` aur `url` ki values identify ki gayi hon.
        *   `deploy` script ki definition note ki gayi ho.

2.  **Task: GitHub Pages Deployment Analysis**
    *   **Description:** Deployed GitHub Pages site ko browser mein open kar ke developer tools ke Network tab mein CSS aur JS files ke loading status aur paths ko check karein. Console mein errors bhi dekhein.
    *   **Acceptance Criteria:**
        *   Deployed site ka URL open kiya gaya ho.
        *   Network tab mein 404 errors ya incorrect paths for CSS/JS files identify kiye gaye hon.
        *   Console tab mein koi relevant errors note kiye gaye hon.

3.  **Task: Docusaurus Configuration Adjustment**
    *   **Description:** `docusaurus.config.js` mein `baseUrl` aur `url` ko GitHub Pages deployment ke mutabiq adjust karein. Yeh ya to `/your-repo-name/` ya phir repo ka sahi naam (e.g., `/AI-DRIVEN_AND_SPEC-DRIVEN_HACKATHON(Failde)/`) aur `url` (`https://username.github.io`) ho sakta hai.
    *   **Acceptance Criteria:**
        *   `docusaurus.config.js` file mein `baseUrl` property update ki gayi ho.
        *   `docusaurus.config.js` file mein `url` property update ki gayi ho.

4.  **Task: Rebuild and Redeploy Docusaurus**
    *   **Description:** Docusaurus project ko rebuild karein aur phir GitHub Pages par redeploy karein.
    *   **Acceptance Criteria:**
        *   `npm run build` command successfully execute hua ho.
        *   `npm run deploy` command successfully execute hua ho.
        *   Deployment complete hone ka confirmation message receive hua ho.

5.  **Task: Verify Frontend Fix**
    *   **Description:** Redeployed GitHub Pages site ko browser mein check karein taake CSS aur JS files sahi tarah se load ho rahin hon aur koi console errors na hon.
    *   **Acceptance Criteria:**
        *   Redeployed site ka URL open kiya gaya ho.
        *   Book ka styling aur interactive elements sahi tarah se kaam kar rahe hon.
        *   Browser developer tools console mein koi CSS ya JavaScript loading errors na hon.

---

## 2. Backend, RAG System, aur Qdrant Data Ingestion Issue

### Task List

1.  **Task: Backend Server Status and Logs Check**
    *   **Description:** Backend server process ki running status check karein aur uske logs ko investigate karein taake errors identify kiye ja sakein.
    *   **Acceptance Criteria:**
        *   Backend server process ki running status confirm ki gayi ho.
        *   Backend logs read kiye gaye hon aur relevant errors (khaas kar ke chatbot interaction ke dauran) note kiye gaye hon.

2.  **Task: FastAPI Endpoint Basic Test**
    *   **Description:** `backend/main.py` (ya jo bhi entry point file ho) ko read karein. Chat endpoint (`/chat`) ko `curl` ya Postman/Insomnia se manually test karein.
    *   **Acceptance Criteria:**
        *   `backend/main.py` file content read kiya gaya ho.
        *   Chat endpoint ki definition aur uski dependencies samjhi gayi hon.
        *   `curl` ya similar tool se chat endpoint par request bhej kar, ek valid response (na ke error) receive hua ho.

3.  **Task: Qdrant Data Ingestion Code Review**
    *   **Description:** `backend/` directory mein Qdrant client ke initialization aur data ingestion logic ko review karein. Confirm karein ke sirf book content hi process kiya ja raha hai.
    *   **Acceptance Criteria:**
        *   Qdrant ingestion se mutalliq files read ki gayi hon.
        *   Data source filtering logic review ki gayi ho aur uski correctness confirm ki gayi ho.
        *   Yeh confirm kiya gaya ho ke sirf `book/docs/` se content uthaya ja raha hai.

4.  **Task: Qdrant Data Content Inspection**
    *   **Description:** Qdrant database mein maujood vectors aur metadata ko inspect karein taake yeh verify ho sake ke ghalat content ingest nahi hua (e.g., "Smart Chat...").
    *   **Acceptance Criteria:**
        *   Qdrant collection ke contents ko list ya sample query kar ke ghalat data (agar koi ho) identify kiya gaya ho.
        *   Agar ghalat data maujood hai, toh uski details note ki gayi hon.

5.  **Task: RAG Logic and Context Handling Review**
    *   **Description:** Backend mein RAG system ki core logic (OpenAI Agents SDK/ChatKit SDK) aur selected text context handling ko review karein.
    *   **Acceptance Criteria:**
        *   RAG system ki core logic files read ki gayi hon.
        *   Selected text context receive aur process karne ka tareeqa samjha gaya ho.
        *   Qdrant se retrieve kiye गए documents ko LLM ko pass karne ka mechanism confirm kiya gaya ho.

6.  **Task: Data Correction and Re-ingestion (Conditional)**
    *   **Description:** Agar Qdrant mein ghalat data milta hai, toh use clear karein aur data ingestion process ko theek kar ke sirf sahi book content ko dobara ingest karein.
    *   **Acceptance Criteria:**
        *   Agar ghalat data tha, toh Qdrant collection clear ki gayi ho ya ghalat vectors delete kiye gaye hon.
        *   Data ingestion logic mein koi ghalati thi, toh usay theek kiya gaya ho.
        *   Sahi book content successfully dobara Qdrant mein ingest kiya gaya ho.

7.  **Task: Full Backend/RAG System Test**
    *   **Description:** Backend ko restart karein aur chatbot ko use kar ke end-to-end test karein.
    *   **Acceptance Criteria:**
        *   Backend server successfully restart hua ho.
        *   Chatbot ko `hi` message bhejte hi, woh sahi tareeqay se respond kare (no error message).
        *   Chatbot, book ke content se related sawalon par sahi jawab de.
        *   Selected text feature RAG system ke saath sahi kaam kare.

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
