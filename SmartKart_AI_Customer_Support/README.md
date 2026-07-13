# SmartKart AI Customer Support Assistant

## Project Overview

SmartKart AI Customer Support Assistant is a Python-based application developed using LangChain and Google Gemini. The project demonstrates how Large Language Models (LLMs) can interact with business tools to provide intelligent responses to customer queries.

The assistant supports common customer service operations such as order tracking, refund eligibility, delivery estimates, and customer account status through LangChain Tool Calling.

---

## Features

- Google Gemini Integration
- LangChain Tool Calling
- Order Status Lookup
- Refund Eligibility Check
- Delivery Estimate
- Customer Account Information
- Conversation History
- Interactive Command Line Interface
- Exception Handling
- Modular Project Structure

---

## Technologies Used

- Python
- LangChain
- Google Gemini
- Pydantic
- Python Dotenv

---

## Project Structure

```
SmartKart_AI_Customer_Support
│
├── app.py
├── assistant.py
├── config.py
├── conversation.py
├── models.py
├── prompts.py
├── tool_executor.py
├── tools.py
├── utils.py
│
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/Shiny212/SAP-BTP-AI-DEVELOPMENT-TRAINING.git
```

### Navigate to the Project Folder

```bash
cd SmartKart_AI_Customer_Support
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file and add your Google Gemini API key.

```text
GOOGLE_API_KEY=YOUR_API_KEY
```

---

## Running the Application

```bash
python app.py
```

---

## Sample Execution

```
Customer : What is the status of order ORD1002?

Assistant :
The status of order ORD1002 is Shipped.
```

```
Customer : Am I eligible for a refund after 15 days?

Assistant :
Yes, you are eligible for a full refund.
```

---

## Available Commands

| Command | Description                  |
| ------- | ---------------------------- |
| history | Display conversation history |
| clear   | Clear conversation history   |
| help    | Display available commands   |
| exit    | Close the application        |

---

## Workflow

```
Customer Query
      │
      ▼
Gemini LLM
      │
      ▼
Tool Selection
      │
      ▼
Business Tool Execution
      │
      ▼
Tool Result
      │
      ▼
Final Response
```

---

## Learning Outcomes

This project demonstrates the following concepts:

- LangChain Tool Calling
- Google Gemini Integration
- Prompt Engineering
- Conversation Memory
- Modular Python Development
- Exception Handling
- Business Logic Integration

---

## Future Enhancements

- Database Integration
- SAP HANA Cloud Integration
- REST API Integration
- Web-Based Interface
- Multi-language Support
- Authentication and Authorization

---

## Author

**Shiny Belsiya**

Bachelor of Engineering – Computer Science and Engineering

SAP BTP AI Development Training

GitHub: https://github.com/Shiny212

---

## License

This project was developed for educational purposes as part of SAP BTP AI Development Training.
