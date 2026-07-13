"""
utils.py

Utility functions used throughout the
SmartKart AI Customer Support project.
"""

import logging

# --------------------------------------------------
# Configure Logging
# --------------------------------------------------

logging.basicConfig(
    level=logging.ERROR,
    format="%(levelname)s : %(message)s"
)

# Hide unnecessary library logs
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("google").setLevel(logging.ERROR)
logging.getLogger("langchain").setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

# --------------------------------------------------
# Print Banner
# --------------------------------------------------

def print_banner(title: str):
    """
    Prints a centered application banner.
    """

    print("=" * 70)
    print(f"{title:^70}")
    print("=" * 70)


# --------------------------------------------------
# Print Section
# --------------------------------------------------

def print_section(title: str):
    """
    Prints a section heading.
    """

    print("\n" + "-" * 70)
    print(title)
    print("-" * 70)


# --------------------------------------------------
# Print Divider
# --------------------------------------------------

def print_divider():
    """
    Prints a divider line.
    """

    print("-" * 70)


# --------------------------------------------------
# Extract Gemini Response
# --------------------------------------------------

def extract_text(response):
    """
    Extracts plain text from a Gemini response.
    """

    if response is None:
        return ""

    # Already a string
    if isinstance(response, str):
        return response.replace('"', "").strip()

    # AIMessage
    if hasattr(response, "content"):

        content = response.content

        # Plain string response
        if isinstance(content, str):
            return content.replace('"', "").strip()

        # Gemini list response
        if isinstance(content, list):

            text_parts = []

            for item in content:

                # Dictionary response
                if isinstance(item, dict):

                    if item.get("type") == "text":

                        text = item.get("text", "")

                        if text:
                            text_parts.append(text)

                # Object response
                elif hasattr(item, "text"):

                    if item.text:
                        text_parts.append(item.text)

            text = "\n".join(text_parts)

            # Remove unwanted quotes
            text = text.replace('"', "")

            return text.strip()

    return str(response).replace('"', "").strip()


# --------------------------------------------------
# Display AI Response
# --------------------------------------------------

def display_response(response):
    """
    Displays the assistant response.
    """

    print(extract_text(response))


# --------------------------------------------------
# Success Message
# --------------------------------------------------

def print_success(message: str):
    """
    Displays a success message.
    """

    print(f"✓ {message}")


# --------------------------------------------------
# Error Message
# --------------------------------------------------

def print_error(message: str):
    """
    Displays an error message.
    """

    print(f"✗ {message}")