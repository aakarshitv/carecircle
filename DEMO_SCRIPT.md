# Demo video script (target 2:00, hard limit 3:00)

Setup before recording: `rm -f carecircle.db && uv run server.py`, then `npx @modelcontextprotocol/inspector`,
connect via Streamable HTTP to `http://localhost:8000/mcp`. Pass `now` = `2026-10-23T16:00` on calls so the demo is stable.

**0:00 – 0:20 Problem.** "My grandparents take four medicines a day. Did they take them? We find out with a phone call — if they pick up. CareCircle lets them just tell Alexa."

**0:20 – 0:35 What it is.** Show `server.py` briefly: "A self-hosted MCP server, Streamable HTTP, protocol 2025-11-25 — the open standard behind Alexa+ integrations." Inspector: Connect → List Tools (4 tools).

**0:35 – 1:00 Family sets up.** Call `add_medication`: Dad, Amlodipine, 5mg, `["08:00","20:00"]`. Again: Dad, Metformin, 500mg, `["13:00"]`. Voice-over: "Alexa, Dad takes Amlodipine at 8 am and 8 pm."

**1:00 – 1:25 Elder checks in.** Call `log_dose`: Dad, "amlodipine", now `2026-10-23T08:20`. Show reply "Logged your 08:00 dose". Voice-over: "Alexa, I took my BP tablet."

**1:25 – 1:55 Family asks.** Call `check_status` then `daily_summary` with now `2026-10-23T16:00`. Show: Amlodipine 08:00 taken, Metformin 13:00 **missed**, Amlodipine 20:00 upcoming. Read the summary aloud: "…You may want to give Dad a call."

**1:55 – 2:15 Wrap.** "Open source, MIT. Next: proactive reminders, missed-dose alerts to family, and Ring integration for caretaking." Show repo URL.
