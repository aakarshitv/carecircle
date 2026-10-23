# CareCircle

**Medication check-ins for elders, by voice, on Alexa+.**

Millions of older adults live alone or away from their children and manage several daily medications.
Apps and pill-box alarms assume a smartphone; a voice assistant doesn't.
CareCircle is a self-hosted [MCP](https://modelcontextprotocol.io) server that gives Alexa+ a simple medication ledger:

- **Elder:** "Alexa, I took my BP tablet." → logged against the nearest scheduled dose.
- **Family:** "Alexa, did Dad take his medicines today?" → taken / missed / upcoming, with a caring summary.

A dose counts as **missed** when nothing is logged within 2 hours of its scheduled time (`MISSED_AFTER` in `server.py`).

## Tools

| Tool | Purpose |
|---|---|
| `add_medication(person, name, dose, times)` | Set a schedule, e.g. Dad, Amlodipine, 5mg, `["08:00","20:00"]` |
| `log_dose(person, medication)` | Record a dose; loose name matching, snaps to the closest scheduled time today |
| `check_status(person)` | Today's doses as structured data: `taken` / `missed` / `upcoming` |
| `daily_summary(person)` | A short spoken summary for a caregiver |

`log_dose`, `check_status` and `daily_summary` take an optional ISO `now` so behaviour is testable and demoable at any time of day.

## Run

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv run server.py
```

Serves MCP over **Streamable HTTP** at `http://localhost:8000/mcp` (protocol `2025-11-25`, official `mcp` Python SDK 2.x). Data is stored in SQLite (`carecircle.db`, override with `CARECIRCLE_DB`; port with `PORT`).

Try it with the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector
```

Choose transport **Streamable HTTP**, URL `http://localhost:8000/mcp`, connect, and call the tools.

To connect from Alexa+ or any remote MCP client, expose the server publicly, e.g. `cloudflared tunnel --url http://localhost:8000`.

## Test

```bash
uv run pytest
```

## Roadmap

- Proactive nudges: Alexa reminds the elder at dose time and notifies family on a missed dose
- Multiple caregivers per person, with consent controls
- Refill tracking ("you have 3 days of Metformin left")
- Ring integration: a missed dose plus no motion at the front door escalates a check-in

## License

MIT
