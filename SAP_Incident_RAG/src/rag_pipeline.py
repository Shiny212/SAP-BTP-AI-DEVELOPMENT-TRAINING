"""
rag_pipeline.py

Enterprise SAP Incident RAG Pipeline

Responsibilities
----------------
1. Load Vector Database
2. Retrieve Relevant Incidents
3. Build Prompt
4. Call Gemini
5. Return Final Answer

Author : Shiny Belsiya
"""

from __future__ import annotations

from src.llm import LLMService
from src.prompt_template import PromptBuilder
from src.retriever import SAPIncidentRetriever


class SAPIncidentRAG:
    """
    Enterprise SAP Incident RAG Pipeline.
    """

    def __init__(self):

        self.retriever = SAPIncidentRetriever()

        self.llm = LLMService.get_llm()

    # ---------------------------------------------------------

    def initialize(
        self,
        documents,
    ) -> None:
        """
        Load or create the vector database.
        """

        self.retriever.initialize(documents)

    # ---------------------------------------------------------

    def ask(
        self,
        question: str,
    ) -> str:
        """
        Execute the complete RAG pipeline.
        """

        documents = self.retriever.retrieve(question)

        messages = PromptBuilder.build_prompt(
            question=question,
            documents=documents,
        )

        response = self.llm.invoke(messages)

        if isinstance(response.content, list):

            answer = []

            for item in response.content:

                if (
                    isinstance(item, dict)
                    and item.get("type") == "text"
              ):
                    answer.append(item["text"])

            return "\n".join(answer)

        return str(response.content)