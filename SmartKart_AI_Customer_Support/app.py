"""
app.py

Entry point of the SmartKart AI Customer Support System.
"""

from assistant import SmartKartAssistant
from utils import print_banner


def main():
    assistant = SmartKartAssistant()

    assistant.chat()


if __name__ == "__main__":
    main()