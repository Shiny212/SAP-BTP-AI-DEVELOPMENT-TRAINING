"""
app.py

Entry point for the
SmartKart AI Customer Support System.
"""

from assistant import SmartKartAssistant
from utils import print_banner


APP_TITLE = "SmartKart AI Customer Support"


def main() -> None:
    """
    Starts the SmartKart application.
    """

    print_banner(APP_TITLE)

    assistant = SmartKartAssistant()

    assistant.chat()


if __name__ == "__main__":
    main()