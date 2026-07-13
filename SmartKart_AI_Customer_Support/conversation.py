"""
conversation.py

Conversation Memory Module
"""

from datetime import datetime

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)


class ConversationMemory:
    """
    Stores and manages conversation history.
    """

    def __init__(self):

        self.messages = []

    # --------------------------------------------------
    # Add User Message
    # --------------------------------------------------

    def add_user_message(self, message: str):

        self.messages.append(
            {
                "timestamp": datetime.now(),
                "message": HumanMessage(content=message)
            }
        )

    # --------------------------------------------------
    # Add AI Message
    # --------------------------------------------------

    def add_ai_message(self, message: str):

        self.messages.append(
            {
                "timestamp": datetime.now(),
                "message": AIMessage(content=message)
            }
        )

    # --------------------------------------------------
    # Get Conversation History
    # --------------------------------------------------

    def get_messages(self):

        return self.messages

    # --------------------------------------------------
    # Clear Conversation
    # --------------------------------------------------

    def clear(self):

        self.messages.clear()

    # --------------------------------------------------
    # Conversation Count
    # --------------------------------------------------

    def total_messages(self):

        return len(self.messages)