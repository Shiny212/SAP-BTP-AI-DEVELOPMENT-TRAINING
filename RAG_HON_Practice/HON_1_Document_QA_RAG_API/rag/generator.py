"""
rag/generator.py

Gemini answer generation using retrieved context.
"""

from __future__ import annotations

from langchain_google_genai import ChatGoogleGenerativeAI

from config.settings import GOOGLE_API_KEY


def get_llm() -> ChatGoogleGenerativeAI:
    """
    Create Gemini chat model.
    """

    return ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        google_api_key=GOOGLE_API_KEY,
        temperature=0,
    )


def generate_answer(
    question: str,
    retrieved_chunks: list[dict],
) -> dict:
    """
    Generate grounded answer using retrieved chunks.
    """

    if not retrieved_chunks:

        return {
            "answer": "Information not available.",
            "sources_used": [],
        }


    context = "\n\n".join(
        [
            chunk["text"]
            for chunk in retrieved_chunks
        ]
    )


    sources = list(
        {
            chunk["source"]
            for chunk in retrieved_chunks
        }
    )


    prompt = f"""
You are an HR policy assistant.

Answer the question ONLY using the provided context.

If the answer is not available in the context,
reply exactly:

Information not available.

Do not use your own knowledge.

Context:

{context}


Question:

{question}
"""


    llm = get_llm()

    response = llm.invoke(
        prompt
    )


    if isinstance(
        response.content,
        list,
    ):

        answer = " ".join(
            [
                item.get("text", "")
                if isinstance(item, dict)
                else str(item)
                for item in response.content
            ]
        ).strip()

    else:

        answer = str(
            response.content
        ).strip()


    return {
        "answer": answer,
        "sources_used": sources,
    }