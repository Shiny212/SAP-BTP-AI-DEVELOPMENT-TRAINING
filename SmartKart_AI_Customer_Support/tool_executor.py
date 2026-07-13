"""
tool_executor.py

Professional Tool Execution Module
"""

from langchain_core.messages import (
    HumanMessage,
    ToolMessage,
)

from config import llm

from conversation import ConversationMemory

from tools import (
    get_order_status,
    check_refund_eligibility,
    get_delivery_estimate,
    get_account_status,
)

from utils import (
    display_response,
    extract_text,
    logger,
)

# --------------------------------------------------
# Debug Mode
# --------------------------------------------------

# True  -> Show tool execution details
# False -> Customer-friendly output only

DEBUG = True

# --------------------------------------------------
# Register Business Tools
# --------------------------------------------------

tools = [
    get_order_status,
    check_refund_eligibility,
    get_delivery_estimate,
    get_account_status,
]

# --------------------------------------------------
# Tool Lookup Dictionary
# --------------------------------------------------

tool_map = {
    tool.name: tool
    for tool in tools
}

# --------------------------------------------------
# Bind Gemini with Tools
# --------------------------------------------------

llm_with_tools = llm.bind_tools(tools)

# --------------------------------------------------
# Conversation Memory
# --------------------------------------------------

memory = ConversationMemory()

# --------------------------------------------------
# Execute Customer Query
# --------------------------------------------------

def execute_customer_query(question: str):
    """
    Executes a customer query using Gemini Tool Calling.
    """

    try:

        memory.add_user_message(question)

        ai_message = llm_with_tools.invoke(question)

        # --------------------------------------------------
        # No Tool Required
        # --------------------------------------------------

        if not ai_message.tool_calls:

            print("\nAssistant:")
            display_response(ai_message)

            memory.add_ai_message(
                extract_text(ai_message)
            )

            return

        messages = [
            HumanMessage(content=question),
            ai_message,
        ]

        # --------------------------------------------------
        # Execute Tool Calls
        # --------------------------------------------------

        for tool_call in ai_message.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            selected_tool = tool_map[tool_name]

            tool_result = selected_tool.invoke(tool_args)

            if DEBUG:

                print("\n")
                print("-" * 70)
                print("Tool Execution")
                print("-" * 70)

                print(f"Tool      : {tool_name}")
                print(f"Arguments : {tool_args}")
                print(f"Result    : {tool_result}")

            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"],
                )
            )

        # --------------------------------------------------
        # Final AI Response
        # --------------------------------------------------

        final_response = llm_with_tools.invoke(messages)

        print("\nAssistant:")

        display_response(final_response)

        memory.add_ai_message(
            extract_text(final_response)
        )

    except Exception as error:

        logger.error(error)

        print("\nAssistant:")
        print(
            "Sorry, something went wrong while processing your request."
        )

# --------------------------------------------------
# Conversation History
# --------------------------------------------------

def show_conversation_history():
    """
    Displays the complete conversation history.
    """

    history = memory.get_messages()

    if not history:

        print("\nNo conversation history available.")
        return

    print("\n")
    print("=" * 70)
    print("Conversation History")
    print("=" * 70)

    for item in history:

        message = item["message"]
        timestamp = item["timestamp"].strftime("%H:%M:%S")

        if message.type == "human":

            print(
                f"\n[{timestamp}] You : {message.content}"
            )

        elif message.type == "ai":

            print(
                f"[{timestamp}] Assistant : {message.content}"
            )

# --------------------------------------------------
# Clear Conversation
# --------------------------------------------------

def clear_conversation():
    """
    Clears the complete conversation history.
    """

    memory.clear()

    print("\n✓ Conversation history cleared.")