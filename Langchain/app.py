import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load variables from .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
   raise ValueError("GOOGLE_API_KEY not found in the .env file.")

print("✅ GOOGLE_API_KEY is configured.")

# Initialize Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=1.0,
    max_retries=2,
)

print("✅ Gemini model initialized.")

# Invoke LLM
response = llm.invoke(
    "Explain LangChain in simple terms for a beginner in three sentences."
)

# Print Response
print(response.content)

# TODO: Replace the prompt with your own question.

exercise_response = llm.invoke(
    "Explain Retrieval-Augmented Generation using a library analogy."
)
print(exercise_response.content)

# ==========================================
# Prompt Templates
# ==========================================

from langchain_core.prompts import ChatPromptTemplate

print("\n========== Prompt Templates ==========\n")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert teacher. Explain concepts clearly for a beginner."),
    ("human", "Explain {topic} using a real-world example.")
])

formatted_prompt = prompt.invoke(
    {"topic": "vector embeddings"}
)

print(formatted_prompt)



# ==========================================
# Output Parser + Basic LCEL Chain
# ==========================================

from langchain_core.output_parsers import StrOutputParser

print("\n========== Basic LCEL Chain ==========\n")

text_parser = StrOutputParser()

basic_chain = prompt | llm | text_parser

result = basic_chain.invoke(
    {"topic": "AI agents"}
)

print(result)



business_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a business AI consultant. Return a concise and practical explanation."
    ),
    (
        "human",
        """Analyze the following AI use case:

Use case: {use_case}
Industry: {industry}

Explain:
1. Business problem
2. How AI can help
3. Required data
4. Expected business value
5. One implementation risk
"""
    )
])

business_chain = business_prompt | llm | StrOutputParser()

business_result = business_chain.invoke({
    "use_case": "Predict which customers are likely to churn",
    "industry": "Telecommunications"
})

print(business_result)



# ==========================================
# Chain Composition
# ==========================================

print("\n========== Chain Composition ==========\n")

summary_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} for a beginner in approximately 150 words."
)

quiz_prompt = ChatPromptTemplate.from_template(
    """Based only on the following explanation, create five multiple-choice questions.
Each question must have four options and provide the correct answer.

Explanation:
{explanation}
"""
)

summary_chain = summary_prompt | llm | StrOutputParser()

quiz_chain = quiz_prompt | llm | StrOutputParser()

explanation = summary_chain.invoke(
    {"topic": "supervised machine learning"}
)

quiz = quiz_chain.invoke(
    {"explanation": explanation}
)

print("=== EXPLANATION ===")
print(explanation)

print("\n=== QUIZ ===")
print(quiz)



# ==========================================
# Learning Plan Generator
# ==========================================

print("\n========== Learning Plan Generator ==========\n")

learning_prompt = ChatPromptTemplate.from_template(
    """You are an expert technical trainer.

Create a 7-day learning plan.

Job role: {role}
Topic: {topic}
Experience level: {level}

For each day provide:
- Learning objective
- Topics
- One hands-on task
- Expected outcome

Keep the plan practical.
"""
)

learning_chain = learning_prompt | llm | StrOutputParser()

plan = learning_chain.invoke(
    {
        "role": "SAP Developer",
        "topic": "Generative AI and LangChain",
        "level": "Beginner",
    }
)

print(plan)



# ==========================================
# Structured Output using Pydantic
# ==========================================

from pydantic import BaseModel, Field
from typing import Literal

print("\n========== Structured Output ==========\n")

class SupportTicket(BaseModel):
    category: Literal[
        "Billing",
        "Technical",
        "Account",
        "Delivery",
        "Other"
    ] = Field(description="Primary ticket category")

    priority: Literal[
        "High",
        "Medium",
        "Low"
    ] = Field(description="Urgency of the issue")

    sentiment: Literal[
        "Positive",
        "Neutral",
        "Negative"
    ] = Field(description="Customer sentiment")

    summary: str = Field(
        description="Short summary of the customer problem"
    )

    recommended_team: str = Field(
        description="Team that should handle the issue"
    )

structured_llm = llm.with_structured_output(SupportTicket)

ticket_text = """
I have been charged twice for my subscription this month.
I contacted support yesterday but have not received a reply.
Please refund the duplicate charge immediately.
"""

ticket = structured_llm.invoke(
    f"Analyze this customer support ticket:\n\n{ticket_text}"
)

print(ticket)
# Convert the validated object to a dictionary
ticket.model_dump()



class EmployeeFeedback(BaseModel):
    main_topic: str
    sentiment: Literal["Positive", "Neutral", "Negative"]
    urgency: Literal["High", "Medium", "Low"]
    summary: str
    action_required: bool

feedback_analyzer = llm.with_structured_output(EmployeeFeedback)

feedback = """
The new internal learning portal is useful, but search is extremely slow.
I need to complete mandatory training by tomorrow and the portal repeatedly times out.
"""

feedback_result = feedback_analyzer.invoke(
    f"Analyze the following employee feedback:\n\n{feedback}"
)

feedback_result


# ==========================================
# Conversation History (Messages)
# ==========================================

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

print("\n========== Conversation History ==========\n")

messages = [
    SystemMessage(
        content="You are a helpful AI tutor. Keep answers concise and beginner-friendly."
    ),
    HumanMessage(
        content="My name is Shiny and I am learning LangChain."
    ),
]

# First AI Response
first_reply = llm.invoke(messages)

print("=== FIRST RESPONSE ===")
print(first_reply.content)

# Add AI response to conversation history
messages.append(first_reply)

# Add another user message
messages.append(
    HumanMessage(
        content="What is my name and what am I learning?"
    )
)

# Second AI Response
second_reply = llm.invoke(messages)

print("\n=== SECOND RESPONSE ===")
print(second_reply.content)


from langchain_core.messages import HumanMessage, SystemMessage

print("\n========== Interactive Chat ==========\n")

chat_history = [
    SystemMessage(
        content="You are a patient LangChain tutor. Give concise, practical answers."
    )
]

print("Type 'exit' to stop.\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("Chat ended.")
        break

    # ADD THIS
    if not user_input:
        print("Please enter a question.\n")
        continue

    chat_history.append(HumanMessage(content=user_input))

    assistant_response = llm.invoke(chat_history)

    chat_history.append(assistant_response)

    if isinstance(assistant_response.content, list):
        print(f"Gemini: {assistant_response.content[0]['text']}\n")
    else:
        print(f"Gemini: {assistant_response.content}\n")


# ==========================================
# LangChain Tools
# ==========================================

from langchain_core.tools import tool

print("\n========== LangChain Tools ==========\n")

@tool
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate the final price after applying a percentage discount."""
    return round(price * (1 - discount_percent / 100), 2)


@tool
def get_order_status(order_id: str) -> str:
    """Get the status of an order from a simulated order database."""
    mock_orders = {
        "ORD-1001": "Shipped",
        "ORD-1002": "Processing",
        "ORD-1003": "Delivered",
    }

    return mock_orders.get(order_id, "Order not found")


print("Discounted Price:")
print(calculate_discount.invoke({
    "price": 1000,
    "discount_percent": 15
}))

print("\nOrder Status:")
print(get_order_status.invoke({
    "order_id": "ORD-1001"
}))



# ==========================================
# Professional Tool Binding
# ==========================================

from langchain_core.messages import HumanMessage, ToolMessage

print("\n========== Professional Tool Binding ==========\n")

tools = [
    calculate_discount,
    get_order_status,
]

tool_map = {tool.name: tool for tool in tools}

llm_with_tools = llm.bind_tools(tools)


def execute_tool_query(question: str):

   from langchain_core.messages import HumanMessage, ToolMessage

def execute_tool_query(question: str):

    print("=" * 70)
    print("User:", question)

    try:
        # Step 1: Ask Gemini
        ai_message = llm_with_tools.invoke(question)

        if not ai_message.tool_calls:
            print("\nGemini Response:")
            print(ai_message.content)
            return

        # Step 2: Conversation history
        messages = [
            HumanMessage(content=question),
            ai_message
        ]

        # Step 3: Execute requested tool(s)
        for tool_call in ai_message.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            selected_tool = tool_map[tool_name]

            tool_result = selected_tool.invoke(tool_args)

            print("\nTool Selected :", tool_name)
            print("Arguments     :", tool_args)
            print("Tool Result   :", tool_result)

            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"]
                )
            )

        # Step 4: Send tool result back to Gemini
        final_response = llm_with_tools.invoke(messages)

        print("\nFinal Answer:")
        print(final_response.content)

    except Exception as error:
        print("\nError:", error)

execute_tool_query(
    "What is the status of order ORD-1002?"
)

execute_tool_query(
    "What is the final price of a ₹2500 product after a 12% discount?"
)


# ==========================================
# Finance Tool Binding
# ==========================================

from langchain_core.tools import tool

print("\n========== Finance Tool Binding ==========\n")

@tool
def calculate_simple_interest(
    principal: float,
    annual_rate: float,
    years: float
) -> float:
    """Calculate simple interest from principal, annual rate percentage, and time in years."""
    return round(principal * annual_rate * years / 100, 2)


tools.append(calculate_simple_interest)

tool_map[calculate_simple_interest.name] = calculate_simple_interest

llm_with_tools = llm.bind_tools(tools)

execute_tool_query(
    "Calculate the simple interest on ₹50,000 at 7.5% per year for 3 years."
)

# ==========================================
# LangChain Documents
# ==========================================

from langchain_core.documents import Document

print("\n========== LangChain Documents ==========\n")

documents = [
    Document(
        page_content="""
        Refund Policy:
        Customers may request a full refund within 30 calendar days of purchase.
        After 30 days, refunds are not normally available unless the product is defective.
        Approved refunds are processed within 5 to 7 business days.
        """,
        metadata={"source": "refund_policy"}
    ),

    Document(
        page_content="""
        Shipping Policy:
        Standard delivery takes 3 to 5 business days.
        Express delivery takes 1 to 2 business days.
        Orders above ₹2,000 qualify for free standard delivery.
        """,
        metadata={"source": "shipping_policy"}
    ),

    Document(
        page_content="""
        Premium Support Policy:
        Premium customers receive 24/7 email and chat support.
        Standard customers receive support Monday to Friday from 9 AM to 6 PM.
        Critical premium incidents have a target initial response time of one hour.
        """,
        metadata={"source": "support_policy"}
    ),
]

print(f"Created {len(documents)} documents.")


# ==========================================
# Text Splitting
# ==========================================

from langchain_text_splitters import RecursiveCharacterTextSplitter

print("\n========== Text Splitting ==========\n")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

print(f"Number of chunks: {len(chunks)}")

for i, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {i} ---")
    print(chunk.page_content.strip())



    # ==========================================
# Embeddings and In-Memory Vector Store
# ==========================================

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

print("\n========== Embeddings & Vector Store ==========\n")

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview",
    output_dimensionality=768,
)

vectorstore = InMemoryVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

print("✅ Vector store created.")



# ==========================================
# Retriever
# ==========================================

print("\n========== Retriever ==========\n")

question = "How long does a refund take after approval?"

retrieved_docs = retriever.invoke(question)

for i, doc in enumerate(retrieved_docs, start=1):
    print(f"--- Retrieved Document {i} ---")
    print(doc.page_content.strip())
    print("Source:", doc.metadata.get("source"))
    print()



    # ==========================================
# Retrieval-Augmented Generation (RAG)
# ==========================================

print("\n========== Retrieval-Augmented Generation ==========\n")

rag_prompt = ChatPromptTemplate.from_template(
    """You are a customer-support knowledge assistant.

Answer the user's question using only the context below.

Rules:
1. Do not invent information.
2. If the answer is not present in the context, say:
   "I do not have enough information in the provided knowledge base."
3. Keep the answer concise.
4. Mention the relevant policy when possible.

Context:
{context}

Question:
{question}
"""
)

def format_docs(docs):
    return "\n\n".join(
        f"Source: {doc.metadata.get('source')}\n{doc.page_content}"
        for doc in docs
    )


def ask_rag(question: str) -> str:
    docs = retriever.invoke(question)
    context = format_docs(docs)

    rag_chain = rag_prompt | llm | StrOutputParser()

    return rag_chain.invoke({
        "context": context,
        "question": question
    })


print(
    ask_rag(
        "Can I get a refund 20 days after purchase?"
    )
)


# ==========================================
# Test the RAG Application
# ==========================================

print("\n========== Testing RAG ==========\n")

questions = [
    "How many days does standard shipping take?",
    "Who receives 24/7 support?",
    "What happens if I ask for a refund after 45 days?",
    "What is the company's office address?"
]

for q in questions:
    print(f"QUESTION: {q}")

    answer = ask_rag(q)

    print("ANSWER:")
    print(answer)

    print("-" * 80)


    # ==========================================
# Structured RAG Output
# ==========================================

from typing import List
from pydantic import BaseModel, Field
from typing import Literal

print("\n========== Structured RAG Output ==========\n")


class CustomerSupportResponse(BaseModel):
    answer: str = Field(
        description="Grounded answer to the customer"
    )

    category: Literal[
        "Refund",
        "Shipping",
        "Support",
        "Other"
    ]

    priority: Literal[
        "High",
        "Medium",
        "Low"
    ]

    needs_human_agent: bool

    source_policies: List[str] = Field(
        description="Knowledge-base sources used for the response"
    )


support_structured_llm = llm.with_structured_output(
    CustomerSupportResponse
)

print("✅ Structured RAG model created.")


# ==========================================
# Final Customer Support Assistant
# ==========================================

print("\n========== Customer Support Assistant ==========\n")

final_support_prompt = ChatPromptTemplate.from_template(
    """You are an AI customer support assistant.

Use only the supplied knowledge-base context.

Customer question:
{question}

Knowledge-base context:
{context}

Instructions:
- Provide a concise grounded answer.
- Never invent a policy.
- Classify the request.
- Set needs_human_agent to true when:
  - the knowledge base is insufficient,
  - the request requires an exception,
  - there is an unresolved urgent complaint.
- Include only sources that appear in the supplied context.
"""
)


def customer_support_assistant(question: str) -> CustomerSupportResponse:

    retrieved_docs = retriever.invoke(question)

    context = format_docs(retrieved_docs)

    chain = final_support_prompt | support_structured_llm

    return chain.invoke(
        {
            "question": question,
            "context": context,
        }
    )


print("✅ Customer Support Assistant Ready.")


# ==========================================
# Test Customer Support Assistant
# ==========================================

print("\n========== Testing Customer Support Assistant ==========\n")

test_questions = [
    "I bought the product 15 days ago. Can I return it for a full refund?",
    "My standard delivery has taken 10 business days and has not arrived.",
    "I am a premium customer. Is chat support available at midnight?",
    "Can I exchange my purchase for a different color?"
]

for question in test_questions:

    print(f"\nCUSTOMER: {question}")

    result = customer_support_assistant(question)

    print(result.model_dump_json(indent=2))

    print("=" * 100)


    # ==========================================
# Interactive Customer Support Assistant
# ==========================================

print("\n========== AI Customer Support Assistant ==========\n")

print("AI Customer Support Assistant")
print("Type 'exit' to stop.\n")

while True:

    question = input("Customer: ").strip()

    if question.lower() == "exit":
        print("Session ended.")
        break

    result = customer_support_assistant(question)

    print("\nAnswer:", result.answer)
    print("Category:", result.category)
    print("Priority:", result.priority)
    print("Human agent required:", result.needs_human_agent)

    if result.source_policies:
        print("Sources:", ", ".join(result.source_policies))
    else:
        print("Sources: None")

    print("-" * 80)