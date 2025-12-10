from typing import Dict, List, Any
import os
from .rag_agent import RAGAgent


class ConversationAgent:
    """
    Conversation Agent that manages chat history and conversation flow
    """

    def __init__(self):
        self.rag_agent = RAGAgent()
        self.conversation_history = []

    def add_to_history(self, user_message: str, bot_response: str):
        """
        Add a conversation turn to the history
        """
        self.conversation_history.append({
            "user": user_message,
            "bot": bot_response,
            "turn": len(self.conversation_history) + 1
        })

    def get_recent_context(self, max_turns: int = 3) -> str:
        """
        Get recent conversation context
        """
        recent_turns = self.conversation_history[-max_turns:] if len(self.conversation_history) >= max_turns else self.conversation_history
        context_parts = []
        for turn in recent_turns:
            context_parts.append(f"User: {turn['user']}")
            context_parts.append(f"Assistant: {turn['bot']}")

        return "\n".join(context_parts)

    def process_message(self, message: str, selected_context: str = None) -> str:
        """
        Process a message in the context of the conversation
        """
        # Use RAG agent to get textbook information
        response = self.rag_agent.process_query(message, selected_context)

        # Add to conversation history
        self.add_to_history(message, response)

        return response