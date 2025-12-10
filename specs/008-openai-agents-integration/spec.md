# OpenAI Agents and ChatKit Integration Specification

## 1. Current State Analysis

### Existing System Architecture
- **Backend**: FastAPI-based RAG system with OpenAI API integration
- **Database**: Qdrant for vector storage, Neon Postgres for chat history
- **Frontend**: Docusaurus with custom React chat widget
- **RAG Flow**: User query → OpenAI embedding → Qdrant search → Context retrieval → OpenAI response generation
- **Chat History**: Stored in Neon Postgres database with conversation_id, user_message, bot_response, selected_text, timestamp

### Current Technologies Stack
- Backend: FastAPI, OpenAI API, Qdrant Client, psycopg2-binary
- Frontend: Docusaurus 3.9.2, React 19, TypeScript
- Database: Qdrant Cloud, Neon Serverless Postgres
- Deployment: GitHub Pages

### Current Functionality
- Text selection detection in frontend
- RAG-based question answering using book content
- Chat history persistence
- Context-aware responses combining selected text and retrieved knowledge

## 2. Requirements for OpenAI Agents Integration

### Agent Types Needed
- **RAG Agent**: Handles document retrieval and context composition
- **Conversation Agent**: Manages chat history and conversation flow
- **Tool Agent**: Orchestrates various tools (Qdrant search, chat history, etc.)

### Agent Decision-Making Capabilities
- Determine when to use selected text context vs. RAG retrieval
- Decide which tools to call based on query type
- Manage conversation memory and context window
- Handle fallback strategies when tools fail

### Memory and Context Management
- Agent-native memory for conversation history
- Context window management for token efficiency
- Long-term memory for persistent user context
- Integration with existing chat history data

### Tool Integration Requirements
- Qdrant search tool for document retrieval
- Chat history tool for conversation context
- Text selection tool for user-highlighted content
- Book content access tool for static information

### Selected Text Context Handling
- Agent must process and incorporate user-selected text
- Priority handling when both selected text and RAG results are available
- Context combination strategies for optimal responses

## 3. Requirements for OpenAI ChatKit Integration

### Frontend Integration Approach
- Replace custom ChatWidget.tsx with OpenAI ChatKit components
- Maintain existing Docusaurus theme integration
- Preserve floating widget functionality
- Keep text selection detection capabilities

### Session Management
- ChatKit session creation and management
- Connection to backend agent system
- Session persistence across page reloads
- User context transfer between sessions

### Backend API Contract Changes
- Agent-based endpoint instead of current /chat API
- Session-based conversation management
- Tool calling integration with frontend
- WebSocket support if needed for real-time updates

### Agent Connection
- ChatKit must connect to OpenAI Agents framework
- Real-time communication between ChatKit and agents
- Proper error handling and fallback mechanisms
- Context transfer from selected text to agent

## 4. Migration Strategy

### Maintaining Existing Functionality
- Preserve current RAG capabilities during migration
- Maintain data integrity of existing chat history
- Keep book content accessibility
- Ensure no disruption to users during transition

### Data Migration Plan
- Existing Neon chat history → Agent memory system
- Migration script for historical data
- Dual system operation during transition period
- Rollback plan if migration issues arise

### API Compatibility
- Maintain backward compatibility where possible
- Gradual API transition with versioning
- Testing of both old and new systems
- Clear endpoint documentation for frontend

### Testing Strategy
- Unit tests for agent tools
- Integration tests for agent workflows
- End-to-end tests for complete flow
- Performance testing for response times

## 5. Success Criteria

### Successful Agent Implementation
- Agents demonstrate autonomous decision-making
- Tool calling works correctly for RAG functionality
- Conversation memory persists appropriately
- Error handling and fallbacks function properly

### Performance Requirements
- Response times under 5 seconds for typical queries
- Support for 100+ concurrent users
- 99.9% uptime for agent services
- Proper token usage optimization

### User Experience Expectations
- Seamless conversation flow with agent responses
- Context-aware responses using selected text and RAG
- No degradation in chat quality compared to current system
- Intuitive interaction with new ChatKit interface

## 6. Constraints and Considerations

### Backward Compatibility
- Existing API consumers must continue to function
- Historical chat data must remain accessible
- Current user workflows preserved during transition

### Security Requirements
- API key management for agent authentication
- Secure session handling
- Proper input validation and sanitization
- Compliance with data privacy regulations

### Cost Implications
- OpenAI Agents API usage costs
- Potential increase in token consumption
- Infrastructure costs for agent execution
- Monitoring and logging expenses

### Technical Limitations
- Agent response times may vary based on complexity
- Context window limitations for long conversations
- Potential complexity in debugging agent workflows
- Dependency on OpenAI's service availability