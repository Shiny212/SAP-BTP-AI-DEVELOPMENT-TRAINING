"""
rag/generator.py

Gemini grounded answer generation.
"""

from __future__ import annotations


from langchain_google_genai import (
    ChatGoogleGenerativeAI,
)


from config.settings import (
    GOOGLE_API_KEY,
)



def get_llm():

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
    Generate answer from retrieved context.
    """


    if not retrieved_chunks:

        return {
            "answer":
            "Information may not be available in documents.",

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
You are an HR assistant.

Answer only using the provided documents.

If the information is not available,
say:

Information may not be available in documents.

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
        )

    else:

        answer = str(
            response.content
        )


    return {
        "answer":
        answer.strip(),

        "sources_used":
        sources,
    }