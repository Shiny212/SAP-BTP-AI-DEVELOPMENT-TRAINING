"""
prompt_template.py

Enterprise Prompt Template for SAP Incident Knowledge Assistant

Responsibilities
----------------
1. Define the System Prompt
2. Build Prompt Templates
3. Format Retrieved Context
4. Generate Final Prompt

Author : Shiny Belsiya
"""

from __future__ import annotations

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate


SYSTEM_PROMPT = """
You are an expert SAP Support Engineer.

Your responsibility is to answer ONLY using the retrieved SAP incident records.

Rules
-----

1. NEVER use your own knowledge.

2. NEVER invent information.

3. If the answer is unavailable, reply exactly:

"I couldn't find this information in the SAP Incident Knowledge Base."

4. If multiple incidents are relevant,
summarize all of them.

5. For every incident you mention, include:

• Incident ID

• SAP Module

• Category

• Priority

• Root Cause

• Resolution

• Owner Team

• Resolution Time

• Status

• Excel Row Number

• Source File

6. At the end, include a section titled:

Source Information

and list:

• Excel File

• Row Number

• SAP Module

7. Format the answer professionally using bullet points.
"""


PROMPT_TEMPLATE = ChatPromptTemplate.from_template(
    """
{system_prompt}

=========================================================
Retrieved SAP Incidents
=========================================================

{context}

=========================================================
User Question
=========================================================

{question}

=========================================================
Answer
=========================================================
"""
)


class PromptBuilder:
    """
    Enterprise Prompt Builder.
    """

    @staticmethod
    def build_context(
        documents: list[Document],
    ) -> str:
        """
        Convert retrieved documents into
        formatted context.
        """

        context = []

        for index, document in enumerate(
            documents,
            start=1,
        ):

            metadata = document.metadata

            context.append(
                f"""
Incident #{index}

{document.page_content}

-------------------------
Metadata
-------------------------

Incident ID : {metadata.get("incident_id")}

SAP Module : {metadata.get("sap_module")}

Category : {metadata.get("category")}

Priority : {metadata.get("priority")}

Owner Team : {metadata.get("owner_team")}

Status : {metadata.get("status")}

Excel Row : {metadata.get("row_number")}

Source File : {metadata.get("source_name")}
"""
            )

        return "\n".join(context)

    @staticmethod
    def build_prompt(
        question: str,
        documents: list[Document],
    ):
        """
        Build LangChain prompt.
        """

        context = PromptBuilder.build_context(
            documents
        )

        return PROMPT_TEMPLATE.format_messages(
            system_prompt=SYSTEM_PROMPT,
            context=context,
            question=question,
        )