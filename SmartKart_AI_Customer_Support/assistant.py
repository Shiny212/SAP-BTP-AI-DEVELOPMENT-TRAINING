"""
assistant.py

SmartKart AI Customer Support Assistant
"""

from prompts import (
    WELCOME_PROMPT,
    EXIT_PROMPT,
)

from tool_executor import (
    execute_customer_query,
    show_conversation_history,
    clear_conversation,
)


class SmartKartAssistant:

    def __init__(self):

        self.version = "2.0.0"

        print("✓ SmartKart AI Assistant Initialized Successfully.\n")

    # -------------------------------------------------

    def show_header(self):

        print("=" * 70)
        print("            SmartKart AI Customer Support")
        print("=" * 70)

        print(f"Version : {self.version}")
        print("Powered By : Gemini 3.1 Flash Lite")
        print("Features :")
        print("✓ Tool Calling")
        print("✓ Pydantic")
        print("✓ Route Selection")
        print("✓ RAG")
        print("✓ FAISS")
        print("✓ Conversation Memory")

        print("-" * 70)

    # -------------------------------------------------

    def show_welcome(self):

        print(WELCOME_PROMPT)

        print("\nCommands")
        print("-" * 30)
        print("history")
        print("clear")
        print("help")
        print("exit")
        print("-" * 70)

    # -------------------------------------------------

    def show_help(self):

        print("\nExample Questions\n")

        print("Where is my order ORD1002?")

        print("Calculate discount for premium with amount 2500")

        print("Delivery to Chennai?")

        print("How many days can I request a refund?")

        print("What payment methods are supported?")

        print("Hello")

        print("-" * 70)

    # -------------------------------------------------

    def chat(self):

        self.show_header()

        self.show_welcome()

        while True:

            question = input("\nYou > ").strip()

            if question == "":
                continue

            if question.lower() == "exit":

                print(EXIT_PROMPT)
                break

            elif question.lower() == "history":

                show_conversation_history()
                continue

            elif question.lower() == "clear":

                clear_conversation()
                continue

            elif question.lower() == "help":

                self.show_help()
                continue

            execute_customer_query(question)