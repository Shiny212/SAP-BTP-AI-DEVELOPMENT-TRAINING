"""
tools.py

Custom LangChain tools for the SAP Support Agent.

Responsibilities:
- Search SAP Knowledge Base
- Check SAP System Status
- Create Support Ticket

These tools are exposed to Gemini using @tool and
executed automatically through LangGraph ToolNode.
"""

from __future__ import annotations

import uuid

from langchain_core.tools import tool

from src.logger import logger, log_tool

# =============================================================================
# Mock SAP Knowledge Base
# =============================================================================

SAP_KB: dict[str, str] = {
    "401 unauthorized": """
Authentication failure detected.

Recommended Checks:
1. Verify SAP BTP Destination credentials.
2. Validate OAuth Client ID and Client Secret.
3. Check OAuth Token expiration.
4. Verify Role Collections.
5. Test the OData endpoint.
6. Restart the iFlow after correcting credentials.
""",

    "cpi": """
SAP Integration Suite (CPI) Troubleshooting:

1. Check Message Monitoring.
2. Verify iFlow deployment.
3. Validate Certificates.
4. Check Adapter configuration.
5. Review Runtime logs.
""",

    "successfactors": """
Employee Replication Troubleshooting:

1. Verify Compound Employee API.
2. Check Employee Replication Job.
3. Validate Middleware Mapping.
4. Verify User Permissions.
""",

    "hana": """
SAP HANA Cloud Troubleshooting:

1. Verify Endpoint URL.
2. Check HDI Container.
3. Verify Database User.
4. Check IP Allow List.
5. Test Database Connectivity.
""",

    "s4hana": """
SAP S/4HANA Troubleshooting:

1. Verify OData Service.
2. Check Gateway Logs.
3. Validate RFC Destination.
4. Review API Error Logs.
""",

    "btp": """
SAP BTP Troubleshooting:

1. Verify Destination Service.
2. Check Service Bindings.
3. Validate Role Collections.
4. Review XSUAA Configuration.
5. Check Application Logs.
"""
}

# =============================================================================
# Mock SAP System Status
# =============================================================================

SYSTEM_STATUS: dict[str, str] = {
    "SAP BTP": "Operational",
    "SAP Integration Suite": "Operational",
    "SAP SuccessFactors": "Operational",
    "SAP S/4HANA": "Operational",
    "SAP HANA Cloud": "Operational",
    "SAP Build Process Automation": "Operational",
}

# =============================================================================
# Tool : Search Knowledge Base
# =============================================================================

@tool
def search_kb(query: str) -> str:
    """
    Search the SAP Knowledge Base.

    Use this tool whenever the user reports an SAP error,
    exception, authentication issue, integration failure,
    replication issue, or connectivity problem.

    Args:
        query: User issue or SAP error message.

    Returns:
        Troubleshooting steps from the mock SAP Knowledge Base.
    """

    log_tool("search_kb")

    query = query.lower()

    for keyword, article in SAP_KB.items():
        if keyword in query:
            logger.info("Knowledge Base Match Found: %s", keyword)
            return article

    logger.info("Knowledge Base Match Not Found")

    return """
No matching SAP Knowledge Base article was found.

Recommended Actions:

1. Review application logs.
2. Check SAP monitoring dashboards.
3. Validate system configuration.
4. Review authentication and authorization.
5. Escalate to SAP Basis if required.
"""


# =============================================================================
# Tool : Check SAP System Status
# =============================================================================

@tool
def check_system_status(system_name: str) -> str:
    """
    Return the operational status of an SAP system.

    Use this tool whenever the health or availability of
    an SAP system needs to be verified.

    Args:
        system_name: SAP system name.

    Returns:
        Operational status.
    """

    log_tool("check_system_status")

    status = SYSTEM_STATUS.get(
        system_name.strip(),
        "Unknown",
    )

    logger.info(
        "System Status Requested | %s | %s",
        system_name,
        status,
    )

    return status


# =============================================================================
# Tool : Create Support Ticket
# =============================================================================

@tool
def create_support_ticket(
    summary: str,
    priority: str,
) -> str:
    """
    Create a mock SAP Support Incident.

    Use this tool only for High priority incidents or when
    escalation is required.

    Args:
        summary: Short description of the issue.
        priority: High, Medium or Low.

    Returns:
        Ticket creation confirmation.
    """

    log_tool("create_support_ticket")

    ticket_id = f"SAP-{uuid.uuid4().hex[:8].upper()}"

    logger.info(
        "Support Ticket Created | %s | %s",
        ticket_id,
        priority,
    )

    logger.info("Issue Summary: %s", summary)

    return f"""
Support Ticket Created Successfully

Ticket ID : {ticket_id}
Priority  : {priority}
Status    : Open
"""


# =============================================================================
# Export All Tools
# =============================================================================

TOOLS = [
    search_kb,
    check_system_status,
    create_support_ticket,
]