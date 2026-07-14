"""
conversation.py

Conversation Memory Management
"""

from datetime import datetime
from typing import List, Dict, Any

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)

# --------------------------------------------------
# System Prompt
# --------------------------------------------------

SYSTEM_PROMPT = """
You are SmartKart AI Customer Support Assistant.

Your responsibilities:
• Be polite, professional, and helpful.
• Use business tools whenever appropriate.
• Use the FAISS knowledge base for:
    - Company Policies
    - Refund Policies
    - Shipping Policies
    - FAQs
• Answer greetings and general conversations naturally.
• Never invent information.
• If information is unavailable, politely inform the customer.
"""


# --------------------------------------------------
# Conversation Memory
# --------------------------------------------------

class ConversationMemory:
    """
    Maintains the complete conversation history
    for SmartKart AI Customer Support.

    Stores:
    - System Messages
    - Human Messages
    - AI Messages
    - Timestamp for every message
    """

    def __init__(self) -> None:
        """
        Initialize conversation with the system prompt.
        """

        self.messages = [
            {
                "message": SystemMessage(
                    content=SYSTEM_PROMPT
                ),
                "timestamp": self._timestamp(),
            }
        ]

    # --------------------------------------------------

    @staticmethod
    def _timestamp() -> datetime:
        """
        Returns the current timestamp.
        """
        return datetime.now()

    # --------------------------------------------------

    def add_user_message(self, message: str) -> None:
        """
        Adds a customer message.
        """

        self.messages.append(
            {
                "message": HumanMessage(
                    content=message
                ),
                "timestamp": self._timestamp(),
            }
        )

    # --------------------------------------------------

    def add_ai_message(self, message: str) -> None:
        """
        Adds an assistant response.
        """

        self.messages.append(
            {
                "message": AIMessage(
                    content=message
                ),
                "timestamp": self._timestamp(),
            }
        )

    # --------------------------------------------------

    def get_messages(self) -> List[Dict[str, Any]]:
        """
        Returns the complete conversation
        including timestamps.
        """

        return self.messages

    # --------------------------------------------------

    def get_chat_history(self):
        """
        Returns only LangChain message objects.

        Used by Gemini and LangChain.
        """

        return [
            item["message"]
            for item in self.messages
        ]

    # --------------------------------------------------

    def clear(self) -> None:
        """
        Clears the conversation while
        preserving the system prompt.
        """

        self.messages = [
            {
                "message": SystemMessage(
                    content=SYSTEM_PROMPT
                ),
                "timestamp": self._timestamp(),
            }
        ]