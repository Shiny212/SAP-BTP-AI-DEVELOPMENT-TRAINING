"""
utils.py

Utility functions for the
SmartKart AI Customer Support project.
"""

import logging
from typing import Any

# --------------------------------------------------
# Configure Logging
# --------------------------------------------------

logging.basicConfig(
    level=logging.ERROR,
    format="%(levelname)s : %(message)s"
)

logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("google").setLevel(logging.ERROR)
logging.getLogger("langchain").setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

# --------------------------------------------------
# Banner
# --------------------------------------------------

def print_banner(title: str) -> None:
    """
    Prints the application banner.
    """

    print("=" * 70)
    print(f"{title:^70}")
    print("=" * 70)


# --------------------------------------------------
# Section
# --------------------------------------------------

def print_section(title: str) -> None:
    """
    Prints a formatted section heading.
    """

    print("\n" + "-" * 70)
    print(title)
    print("-" * 70)


# --------------------------------------------------
# Divider
# --------------------------------------------------

def print_divider() -> None:
    """
    Prints a divider.
    """

    print("-" * 70)


# --------------------------------------------------
# Extract Gemini Response
# --------------------------------------------------

def extract_text(response: Any) -> str:
    """
    Extracts plain text from a Gemini response.
    """

    if response is None:
        return ""

    if isinstance(response, str):
        return response.replace('"', "").strip()

    if hasattr(response, "content"):

        content = response.content

        if isinstance(content, str):
            return content.replace('"', "").strip()

        if isinstance(content, list):

            text_parts = []

            for item in content:

                if isinstance(item, dict):

                    if item.get("type") == "text":

                        text = item.get("text", "")

                        if text:
                            text_parts.append(text)

                elif hasattr(item, "text"):

                    if item.text:
                        text_parts.append(item.text)

            return "\n".join(text_parts).replace('"', "").strip()

    return str(response).replace('"', "").strip()


# --------------------------------------------------
# Display Response
# --------------------------------------------------

def display_response(response: Any) -> None:
    """
    Displays the assistant response.
    """

    print(extract_text(response))


# --------------------------------------------------
# Success Message
# --------------------------------------------------

def print_success(message: str) -> None:
    """
    Displays a success message.
    """

    print(f"✓ {message}")


# --------------------------------------------------
# Error Message
# --------------------------------------------------

def print_error(message: str) -> None:
    """
    Displays an error message.
    """

    print(f"✗ {message}")