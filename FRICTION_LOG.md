# Friction log

## 1. Following the MCP Python quickstart on SDK 2.x
- **Task:** Create a Streamable HTTP MCP server for Alexa+.
- **Steps:** `uv add mcp` (installed 2.3.0), wrote `from mcp.server.fastmcp import FastMCP`, `FastMCP("CareCircle", host=..., port=...)` as most tutorials show.
- **Expected:** Server starts.
- **Actual:** `ModuleNotFoundError: No module named 'mcp.server.fastmcp'`. The message helpfully names `mcp.server.mcpserver.MCPServer` and links the migration guide.
- **Severity:** Medium (blocks every 1.x tutorial; ~10 min lost).
- **Workaround:** Switched to `MCPServer`; inspected signatures to find that `host`/`port` moved from the constructor to `run(transport="streamable-http", host=..., port=...)`.
- **Suggestion:** Pin hackathon/Alexa+ MCP samples to SDK 2.x, and mention the `run()` keyword arguments in the migration guide's FastMCP section.

## 2. Demoing the server through Alexa+
- **Task:** Show our MCP server answering a real Alexa+ utterance.
- **Steps:** Looked through the hackathon resources for a way to point Alexa+ (or a simulator) at a self-hosted Streamable HTTP endpoint.
- **Expected:** A test console where we can type/speak an utterance and see it routed to our tools.
- **Actual:** No such path available to us during the hackathon; demoed with the generic MCP Inspector instead.
- **Severity:** High for demo fidelity (judges don't see the voice experience).
- **Workaround:** MCP Inspector over Streamable HTTP, with voice-over of the intended utterances.
- **Suggestion:** An Alexa+ MCP test console (accepts a tunnelled URL, shows the routed tool calls).

## 3. Proactive notifications
- **Task:** Alert family when a dose is missed.
- **Steps:** Searched for how an MCP server can initiate an Alexa+ notification.
- **Expected:** A documented mechanism.
- **Actual:** Not found; MCP tools are request/response only from our side.
- **Severity:** Medium (our main next feature).
- **Workaround:** Deferred; family must ask.
- **Suggestion:** Document proactive/notification support for Alexa+ MCP integrations.
