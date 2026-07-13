"""
assistant.py

Interactive SmartKart AI Customer Support Assistant.
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
    """
    SmartKart AI Customer Support Assistant.
    """

    def __init__(self):

        self.version = "1.0.0"

        print("✓ SmartKart Assistant Initialized Successfully.\n")

    # --------------------------------------------------
    # Display Header
    # --------------------------------------------------

    def show_header(self):

        print("=" * 70)
        print("               SmartKart AI Customer Support")
        print("=" * 70)

        print(f"Version    : {self.version}")
        print("Powered By : LangChain + Gemini")
        print("-" * 70)

    # --------------------------------------------------
    # Display Welcome Message
    # --------------------------------------------------

    def show_welcome(self):

        print(WELCOME_PROMPT)

        print("\nAvailable Commands")
        print("-" * 30)
        print("history  -> Show conversation history")
        print("clear    -> Clear conversation history")
        print("help     -> Show available commands")
        print("exit     -> Exit application")

        print("-" * 70)

    # --------------------------------------------------
    # Display Help
    # --------------------------------------------------

    def show_help(self):

        print("\nAvailable Commands")
        print("-" * 30)

        print("history  -> Show conversation history")
        print("clear    -> Clear conversation history")
        print("help     -> Show available commands")
        print("exit     -> Exit application")

        print("-" * 70)

    # --------------------------------------------------
    # Start Chat Session
    # --------------------------------------------------

    def chat(self):

        self.show_header()

        self.show_welcome()

        while True:

            question = input("\nYou > ").strip()

            if not question:
                continue

            command = question.lower()

            # Exit
            if command == "exit":

                print("\n" + EXIT_PROMPT)
                break

            # History
            elif command == "history":

                show_conversation_history()
                continue

            # Clear
            elif command == "clear":

                clear_conversation()
                continue

            # Help
            elif command == "help":

                self.show_help()
                continue

            # Execute Customer Query
            execute_customer_query(question)