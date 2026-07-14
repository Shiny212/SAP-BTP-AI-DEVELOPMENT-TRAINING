"""
prompts.py

Prompt Templates
"""

from langchain_core.prompts import ChatPromptTemplate
# --------------------------------------------------
# Welcome & Exit Messages
# --------------------------------------------------

WELCOME_PROMPT = """
Welcome to SmartKart AI Customer Support!

I can help you with:

• Order Status
• Delivery Information
• Discount Calculation
• Refund Policy
• Return Policy
• Shipping Policy
• General Questions

Type your question below to get started.
"""


EXIT_PROMPT = """
Thank you for using SmartKart AI Customer Support.

Have a great day!
"""


# --------------------------------------------------
# Ticket Classification Prompt
# --------------------------------------------------

TICKET_CLASSIFIER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are SmartKart AI Customer Support Assistant.

Your task is to analyze the customer's query and generate a structured support ticket.

Populate ALL of the following fields:

1. category
2. priority
3. sentiment
4. summary
5. recommended_team
6. requires_human_agent
7. route

Routing Rules
-------------

Select ONLY ONE route.

TOOL
Use for:
- Order Status
- Discount Calculation
- Delivery Charge
- Delivery Estimate

RAG
Use for:
- Refund Policy
- Return Policy
- Shipping Policy
- Delivery Policy
- Payment Policy
- Premium Membership
- FAQs
- Company Policies

LLM
Use for:
- Greetings
- General Conversation
- Casual Questions

Output Rules
------------

- Return ONLY structured output.
- Do not include explanations.
- Do not include markdown.
- Route must be exactly one of:
  TOOL
  RAG
  LLM
"""
        ),
        (
            "human",
            "{query}"
        )
    ]
)