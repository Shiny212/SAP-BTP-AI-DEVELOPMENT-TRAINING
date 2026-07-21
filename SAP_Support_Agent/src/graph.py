"""
graph.py

Defines the LangGraph workflow for the SAP Support Agent.

Workflow:
START
   │
   ▼
 Agent
   │
   ├──────────────► ToolNode (if tool call)
   │                    │
   │                    ▼
   │              Classification
   │                    │
   ▼                    ▼
Classification ─────► Priority
                         │
                         ▼
                      Draft
                         │
                         ▼
                     Human Review
                         │
                  Approved?
                  │       │
                  ▼       ▼
               Final    Draft
                  │
                  ▼
            Post Process
                  │
                  ▼
                 END
"""

from __future__ import annotations

from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from src.state import SupportAgentState
from src.tools import TOOLS
from src.memory import get_checkpointer

from src.nodes import (
    call_model,
    classify_issue_node,
    assign_priority_node,
    draft_response_node,
    human_review_node,
    final_response_node,
    post_process_node,
)

from src.routes import (
    route_after_classification,
    route_after_priority,
    route_after_review,
    route_after_final,
)

# ============================================================
# Build Workflow
# ============================================================

workflow = StateGraph(SupportAgentState)

# ============================================================
# Register Nodes
# ============================================================

workflow.add_node("agent", call_model)

workflow.add_node(
    "tools",
    ToolNode(TOOLS),
)

workflow.add_node(
    "classification",
    classify_issue_node,
)

workflow.add_node(
    "priority",
    assign_priority_node,
)

workflow.add_node(
    "draft",
    draft_response_node,
)

workflow.add_node(
    "review",
    human_review_node,
)

workflow.add_node(
    "final",
    final_response_node,
)

workflow.add_node(
    "post_process",
    post_process_node,
)

# ============================================================
# Graph Flow
# ============================================================

workflow.add_edge(
    START,
    "agent",
)

# Tool Routing
workflow.add_conditional_edges(
    "agent",
    tools_condition,
)

# Continue after tool execution
workflow.add_edge(
    "tools",
    "classification",
)

# Classification → Priority
workflow.add_conditional_edges(
    "classification",
    route_after_classification,
)

# Priority → Draft
workflow.add_conditional_edges(
    "priority",
    route_after_priority,
)

# Draft → Review
workflow.add_edge(
    "draft",
    "review",
)

# Review → Final or regenerate draft
workflow.add_conditional_edges(
    "review",
    route_after_review,
)

# Final → Post Process
workflow.add_conditional_edges(
    "final",
    route_after_final,
)

# Finish
workflow.add_edge(
    "post_process",
    END,
)

# ============================================================
# Compile Graph
# ============================================================

app = workflow.compile(
    checkpointer=get_checkpointer()
)