"""
tool_executor.py

Central orchestration module for the
SmartKart AI Customer Support Assistant.

Responsibilities
----------------
• Pydantic ticket classification
• Intelligent route selection
• LangChain tool calling
• FAISS RAG retrieval
• Conversation memory
• CLI & Streamlit integration

Author:
Shiny Belsiya
"""

from langchain_core.prompts import ChatPromptTemplate

from config import llm
from conversation import ConversationMemory
from models import SupportTicket
from prompts import TICKET_CLASSIFIER_PROMPT
from rag import ask_rag

# Import Business Tools
from tools import (
    check_order_status,
    calculate_discount,
    calculate_delivery_charge,
    get_estimated_delivery,
)

from utils import (
    print_section,
    print_divider,
    print_success,
    print_error,
    extract_text,
    logger,
)

# --------------------------------------------------
# UI & Output Section Constants
# --------------------------------------------------
SECTION_TICKET = "Structured Support Ticket"
SECTION_ROUTE = "Route Selected"
SECTION_TOOL_REQ = "Tool Requested"
SECTION_TOOL_EXE = "Tool Execution"
SECTION_TOOL_RES = "Tool Result"
SECTION_ASSISTANT = "SmartKart Assistant"
SECTION_HISTORY = "Conversation History"
SECTION_KNOWLEDGE_BASE = "Knowledge Base Search"
SECTION_LLM_CONV = "LLM Conversation"

# --------------------------------------------------
# Error & Static Message Constants
# --------------------------------------------------
GENERIC_ERROR = (
    "Sorry, I couldn't complete your request "
    "because an internal error occurred."
)

# --------------------------------------------------
# Constants & Tools Setup
# --------------------------------------------------
# Global Default Memory (For CLI/app.py session)
_cli_memory = ConversationMemory()

# Map tool names to actual functions for dynamic invocation
TOOL_MAP = {
    "check_order_status": check_order_status,
    "calculate_discount": calculate_discount,
    "calculate_delivery_charge": calculate_delivery_charge,
    "get_estimated_delivery": get_estimated_delivery,
}

# LangChain-recommended formatting template for tool results
TOOL_RESPONSE_PROMPT = ChatPromptTemplate.from_template(
    """
You are SmartKart AI Customer Support Assistant.

Use ONLY the following tool result to answer.

Customer Question:
{question}

Tool Result:
{result}

Provide a professional, concise and customer-friendly response.

Do not invent additional information.
"""
)

# Globally compiled response chain for performance efficiency
TOOL_RESPONSE_CHAIN = TOOL_RESPONSE_PROMPT | llm

# Move the structured output LLM compilation globally to avoid recreation on every query
STRUCTURED_LLM = llm.with_structured_output(SupportTicket)

# Globally compile classifier chain
CLASSIFIER_CHAIN = TICKET_CLASSIFIER_PROMPT | STRUCTURED_LLM

# Make the tools list immutable using a tuple as it doesn't change at runtime
TOOLS = (
    check_order_status,
    calculate_discount,
    calculate_delivery_charge,
    get_estimated_delivery,
)

# Bind tools to the LLM for tool calling
llm_with_tools = llm.bind_tools(TOOLS)


# --------------------------------------------------
# Ticket Classification & Routing
# --------------------------------------------------
def classify_ticket(query: str) -> SupportTicket:
    """
    Uses Gemini structured output with Pydantic to classify the incoming query 
    and select the optimal execution route.
    """
    return CLASSIFIER_CHAIN.invoke({"query": query})


# --------------------------------------------------
# Route Handling Execution
# --------------------------------------------------
def handle_tool_route(query: str, memory: ConversationMemory) -> str:
    """
    Handles queries routed to business tools. Invokes Gemini with 
    tool definitions, executes the tool, and formulates a final response.
    """
    # Let LLM decide which tool to call based on latest memory state
    response = llm_with_tools.invoke(memory.get_chat_history())
    
    # Clean check: If no tool calls are present, directly return the model's text response.
    if not response.tool_calls:
        return extract_text(response)
        
    tool_call = response.tool_calls[0]
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]
    
    # Show tool request details using centralized constants
    print_section(SECTION_TOOL_REQ)
    print(f"Tool Name : {tool_name}")
    print("Arguments :")
    if tool_args:
        for key, value in tool_args.items():
            print(f"  {key:<15}: {value}")
    else:
        print("  No arguments")
    
    # Safe lookup and execution
    tool = TOOL_MAP.get(tool_name)
    if tool is None:
        return (
            "Sorry, the requested operation "
            "is currently unavailable."
        )
        
    try:
        tool_output = tool.invoke(tool_args)
        
        # Show tool execution details for demos/viva
        print_section(SECTION_TOOL_EXE)
        print(f"Tool      : {tool_name}")
        print("Arguments :")
        if tool_args:
            for key, value in tool_args.items():
                print(f"  {key:<15}: {value}")
        else:
            print("  No arguments")
        
        print_section(SECTION_TOOL_RES)
        if isinstance(tool_output, dict):
            for key, value in tool_output.items():
                print(f"{key:<20}: {value}")
        else:
            print(tool_output)
        
        # Invoke pre-compiled chain to compile response without raw f-strings
        final_response = TOOL_RESPONSE_CHAIN.invoke(
            {
                "question": query,
                "result": tool_output,
            }
        )
        return extract_text(final_response)
        
    except Exception as error:
        # Log exception natively for core debug traceability and print to console cleanly
        logger.exception(error)
        print_error(str(error))
        return GENERIC_ERROR


def handle_rag_route(query: str) -> str:
    """
    Handles policy and FAQ queries using the FAISS knowledge base.
    """
    try:
        print_section(SECTION_KNOWLEDGE_BASE)
        return ask_rag(query)
    except Exception as error:
        logger.exception(error)
        print_error(str(error))
        return (
            "Sorry, I couldn't retrieve "
            "the requested information "
            "from the SmartKart knowledge base."
        )


def handle_llm_route(memory: ConversationMemory) -> str:
    """
    Handles greetings and standard chatter by engaging the main LLM.
    """
    print_section(SECTION_LLM_CONV)
    response = llm.invoke(memory.get_chat_history())
    return extract_text(response)


# --------------------------------------------------
# Main Customer Query Handler
# --------------------------------------------------
def execute_customer_query(query: str, memory: ConversationMemory = None) -> str:
    """
    Main entry point for query resolution. Classifies user query, 
    routes the execution dynamically, and formats gorgeous logs.
    """
    # Stop empty or whitespace-only inputs immediately
    query = query.strip()
    if not query:
        return "Please enter your question."

    active_memory = memory if memory is not None else _cli_memory
    
    # Secure user message inside memory before processing classification.
    # This preserves conversation full state context even if downstream components break.
    active_memory.add_user_message(query)
    
    try:
        # 1. Classify ticket and select route
        ticket = classify_ticket(query)
        
        # Professional structured ticket printing layout
        print_section(SECTION_TICKET)
        print(f"Category              : {ticket.category}")
        print(f"Priority              : {ticket.priority}")
        print(f"Sentiment             : {ticket.sentiment}")
        print(f"Summary               : {ticket.summary}")
        print(f"Recommended Team      : {ticket.recommended_team}")
        print(f"Requires Human Agent  : {ticket.requires_human_agent}")
        print(f"Route                 : {ticket.route}")
        
        # Normalize the route state before printing and routing decisions
        route = ticket.route.upper()
        
        # Dedicated section showcasing chosen execution route with cleaner, aligned layout
        print_section(SECTION_ROUTE)
        print(f"Selected Route  : {route}")
        
        if route == "TOOL":
            ai_response = handle_tool_route(query, active_memory)
        elif route == "RAG":
            ai_response = handle_rag_route(query)
        else:
            ai_response = handle_llm_route(active_memory)
            
        # 2. Save calculated response to active memory
        active_memory.add_ai_message(ai_response)
        
        # 3. Display response if executed inside the CLI app
        if memory is None:
            # Display customer response banner using the updated SECTION_ASSISTANT layout heading
            print_section(SECTION_ASSISTANT)
            print(ai_response)
            print_divider()
            
        return ai_response
        
    except Exception as error:
        # Native logging integration for robust error-catching tracebacks
        logger.exception(error)
        print_error(str(error))
        
        # Preserve the failure error message inside the conversation memory window
        active_memory.add_ai_message(GENERIC_ERROR)
        return GENERIC_ERROR


# --------------------------------------------------
# Conversation History Helpers (CLI/app.py compatible)
# --------------------------------------------------
def show_conversation_history() -> None:
    """
    Retrieves and displays conversational history. Used in CLI.
    """
    print_section(SECTION_HISTORY)
    messages = _cli_memory.get_messages()
    
    if len(messages) <= 1:
        print("No prior conversation history recorded.")
        print_divider()
        return

    # Skip system prompt at index 0 and loop without needing unused enumerate indexing
    for item in messages[1:]:
        msg = item["message"]
        timestamp = item["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        
        sender = "You" if msg.type == "human" else "Assistant"
        print(f"[{timestamp}] {sender}: {msg.content}")
        
    print_divider()


def clear_conversation() -> None:
    """
    Wipes the conversational memory cleanly.
    """
    _cli_memory.clear()
    print_success("Conversation history cleared successfully.")