"""
rag/query_rewriter.py

Converts follow-up questions into
standalone questions using conversation history.
"""

from __future__ import annotations


from langchain_google_genai import (
    ChatGoogleGenerativeAI,
)


from config.settings import GOOGLE_API_KEY



def get_llm():

    return ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        google_api_key=GOOGLE_API_KEY,
        temperature=0,
    )



def rewrite_question(
    question: str,
    history: list[dict],
) -> str:
    """
    Rewrite follow-up question using history.
    """


    # First question in session
    if not history:

        return question



    conversation = "\n".join(
        [
            f"User: {item['question']}\n"
            f"Assistant: {item['answer']}"
            for item in history
        ]
    )


    prompt = f"""
You are a question rewriting assistant.

Convert the follow-up question into a
clear standalone question.

Use the conversation history.

Conversation:

{conversation}


Follow-up question:

{question}


Return only the standalone question.
"""


    llm = get_llm()


    response = llm.invoke(
        prompt
    )


    if isinstance(
        response.content,
        list,
    ):

        rewritten = " ".join(
            [
                item.get("text", "")
                if isinstance(item, dict)
                else str(item)
                for item in response.content
            ]
        )

    else:

        rewritten = str(
            response.content
        )


    return rewritten.strip()