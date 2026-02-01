from typing import TypedDict, Optional, Any

class ToolResult(TypedDict):
    reply_text: str
    data: Optional[dict[str, Any]]
