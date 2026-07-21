from pathlib import Path

from src.graph import app

png = app.get_graph().draw_mermaid_png()

Path("workflow_graph.png").write_bytes(png)

print("Graph generated successfully.")