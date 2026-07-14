# 🛒 SmartKart AI Customer Support Assistant

An intelligent AI-powered customer support chatbot built using **LangChain**, **Google Gemini 3.1 Flash Lite**, **FAISS**, **HuggingFace Embeddings**, and **Streamlit**.

The chatbot can intelligently route customer queries to:

- 🔧 Business Tools
- 📚 Retrieval-Augmented Generation (RAG)
- 🤖 General LLM Conversation

---

# Features

- ✅ Gemini 3.1 Flash Lite
- ✅ LangChain
- ✅ Pydantic Structured Output
- ✅ Intelligent Route Selection
- ✅ Tool Calling
- ✅ FAISS Vector Database
- ✅ HuggingFace Embeddings
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Conversation Memory
- ✅ CLI Application
- ✅ Streamlit Chatbot

---

# Project Structure

```
SmartKart_AI_Customer_Support/
│
├── app.py
├── assistant.py
├── config.py
├── conversation.py
├── models.py
├── prompts.py
├── rag.py
├── tool_executor.py
├── tools.py
├── utils.py
├── streamlit_app.py
├── requirements.txt
├── .env
│
├── knowledge_base/
│   └── smartkart_policies.txt
│
└── README.md
```

---

# Technologies Used

- Python
- LangChain
- Google Gemini 3.1 Flash Lite
- FAISS
- HuggingFace Embeddings
- Pydantic
- Streamlit
- Python Dotenv

---

# AI Workflow

```
Customer Query
       │
       ▼
Pydantic Classification
       │
       ▼
Route Selection
 ┌───────────────┐
 │ TOOL │ RAG │ LLM │
 └───────────────┘
       │
       ▼
Gemini Response
       │
       ▼
Conversation Memory
```

---

# Route Selection

## TOOL

Handles:

- Order Status
- Discount Calculation
- Delivery Charge
- Estimated Delivery

---

## RAG

Uses FAISS Knowledge Base.

Handles:

- Refund Policy
- Return Policy
- Shipping Policy
- Company Policies
- FAQs
- Premium Membership

---

## LLM

Handles:

- Greetings
- General Conversation
- Casual Questions

---

# Installation

Clone the repository.

```bash
git clone https://github.com/<your-username>/SmartKart_AI_Customer_Support.git
```

Go into the project.

```bash
cd SmartKart_AI_Customer_Support
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```
GOOGLE_API_KEY=YOUR_API_KEY
```

---

# Run CLI Version

```bash
python app.py
```

---

# Run Streamlit Version

```bash
streamlit run streamlit_app.py
```

---

# Sample Questions

### Tool Calling

```
Track my order ORD102
```

```
Calculate discount for premium customer with amount 3500
```

```
Delivery charge for ₹700
```

---

### RAG

```
What is SmartKart's refund policy?
```

```
Explain the return policy.
```

```
Tell me about premium membership.
```

---

### LLM

```
Hello
```

```
How are you?
```

```
Thank you
```

---

# Future Enhancements

- Database Integration
- User Authentication
- Order Management APIs
- Multi-language Support
- Voice Assistant
- Sentiment Analytics
- Admin Dashboard

---

# Author

**Shiny Belsiya**

SAP BTP AI Development Project

Powered by Google Gemini + LangChain + FAISS + HuggingFace Embeddings
