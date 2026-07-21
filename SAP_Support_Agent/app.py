"""
app.py

Console application for the SAP Support Agent.
"""

from __future__ import annotations

import uuid

from langchain_core.messages import HumanMessage

from src.graph import app
from src.config import APPLICATION_NAME
from src.logger import logger


def chat() -> None:
    """
    Starts the SAP Support Agent console application.
    """

    print("=" * 70)
    print(f"{APPLICATION_NAME}")
    print("Type 'exit' or 'quit' to end the session.")
    print("=" * 70)

    thread_id = str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    logger.info("New session started: %s", thread_id)

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            if user_input.lower() in {"exit", "quit"}:
                print("\nThank you for using SAP Support Agent.")
                logger.info("Session ended: %s", thread_id)
                break

            result = app.invoke(
                {
                    "messages": [
                        HumanMessage(content=user_input)
                    ]
                },
                config=config,
            )

            # --------------------------------------------------------
            # Display the polished final response if available
            # --------------------------------------------------------
            if result.get("final_response"):
                print(f"\nAssistant:\n{result['final_response']}")
            else:
                messages = result.get("messages", [])

                if messages:
                    print(f"\nAssistant:\n{messages[-1].content}")
                else:
                    print("\nAssistant: No response generated.")

        except KeyboardInterrupt:
            print("\n\nSession interrupted.")
            logger.info("Session interrupted by user.")
            break

        except Exception as exc:
            logger.exception(exc)
            print("\nAn unexpected error occurred.")
            print(exc)


if __name__ == "__main__":
    chat()