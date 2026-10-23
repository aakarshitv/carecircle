"""CareCircle: a medication check-in MCP server for Alexa+.

Elders tell Alexa when they take a dose; family asks Alexa whether they did.
Runs as a self-hosted MCP server over Streamable HTTP.
"""
import json
import os
import sqlite3
from datetime import datetime, timedelta

from mcp.server.mcpserver import MCPServer

MISSED_AFTER = timedelta(hours=2)  # a dose with no check-in this long after its time is "missed"
DB_PATH = os.environ.get("CARECIRCLE_DB", "carecircle.db")

mcp = MCPServer("CareCircle", version="0.1.0", instructions="Medication check-ins for elders and their families.")


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS meds (
            person TEXT NOT NULL, name TEXT NOT NULL, dose TEXT NOT NULL, times TEXT NOT NULL,
            PRIMARY KEY (person, name) ON CONFLICT REPLACE);
        CREATE TABLE IF NOT EXISTS doses (
            person TEXT NOT NULL, name TEXT NOT NULL, slot TEXT NOT NULL, taken_at TEXT NOT NULL,
            UNIQUE (person, name, slot) ON CONFLICT IGNORE);
    """)
    return conn


def norm(s: str) -> str:
    return s.strip().lower()


def find_med(conn, person, medication):
    """Match a spoken medication name loosely ("BP tablet" -> nothing, "amlodipine" -> Amlodipine)."""
    meds = conn.execute("SELECT * FROM meds WHERE person = ?", (norm(person),)).fetchall()
    m = norm(medication)
    for row in meds:
        if m == row["name"] or m in row["name"] or row["name"] in m:
            return row
    return meds[0] if len(meds) == 1 else None


def schedule(conn, person, now):
    """Today's doses for a person, each tagged taken / missed / upcoming."""
    today = now.date().isoformat()
    taken = {(r["name"], r["slot"]): r["taken_at"] for r in conn.execute(
        "SELECT * FROM doses WHERE person = ? AND slot LIKE ?", (norm(person), today + "%"))}
    out = []
    for med in conn.execute("SELECT * FROM meds WHERE person = ? ORDER BY name", (norm(person),)):
        for t in json.loads(med["times"]):
            slot = f"{today}T{t}"
            due = datetime.fromisoformat(slot)
            if (med["name"], slot) in taken:
                status = "taken"
            elif now > due + MISSED_AFTER:
                status = "missed"
            else:
                status = "upcoming"
            out.append({"medication": med["name"], "dose": med["dose"], "time": t, "status": status,
                        "taken_at": taken.get((med["name"], slot))})
    return sorted(out, key=lambda d: d["time"])


@mcp.tool()
def add_medication(person: str, name: str, dose: str, times: list[str]) -> str:
    """Add or replace a medication schedule. times are 24h "HH:MM", e.g. ["08:00", "20:00"]."""
    for t in times:
        datetime.strptime(t, "%H:%M")  # reject bad times early
    with db() as conn:
        conn.execute("INSERT INTO meds VALUES (?, ?, ?, ?)",
                     (norm(person), norm(name), dose, json.dumps(sorted(times))))
    return f"Okay. {person} takes {dose} of {name} at {', '.join(sorted(times))}."


@mcp.tool()
def log_dose(person: str, medication: str, now: str | None = None) -> str:
    """Record that a person just took a medication. Matches it to the closest scheduled time today."""
    now_dt = datetime.fromisoformat(now) if now else datetime.now()
    with db() as conn:
        med = find_med(conn, person, medication)
        if not med:
            return f"I couldn't find {medication} for {person}. Ask a family member to add it first."
        times = json.loads(med["times"])
        today = now_dt.date().isoformat()
        best = min(times, key=lambda t: abs(now_dt - datetime.fromisoformat(f"{today}T{t}")))
        conn.execute("INSERT INTO doses VALUES (?, ?, ?, ?)",
                     (norm(person), med["name"], f"{today}T{best}", now_dt.isoformat(timespec="minutes")))
    return f"Got it, {person}. Logged your {best} dose of {med['name']}."


@mcp.tool()
def check_status(person: str, now: str | None = None) -> dict:
    """Today's medication status for a person: which doses were taken, missed, or are upcoming."""
    now_dt = datetime.fromisoformat(now) if now else datetime.now()
    with db() as conn:
        doses = schedule(conn, person, now_dt)
    if not doses:
        return {"person": person, "doses": [], "message": f"No medications set up for {person}."}
    return {"person": person, "doses": doses}


@mcp.tool()
def daily_summary(person: str, now: str | None = None) -> str:
    """A short, caring summary of today's medications that Alexa can read to a family member."""
    status = check_status(person, now)
    doses = status["doses"]
    if not doses:
        return status["message"]
    taken = [d for d in doses if d["status"] == "taken"]
    missed = [d for d in doses if d["status"] == "missed"]
    upcoming = [d for d in doses if d["status"] == "upcoming"]
    parts = [f"{person} has taken {len(taken)} of {len(doses)} doses today."]
    if missed:
        parts.append("Missed: " + ", ".join(f"{d['medication']} at {d['time']}" for d in missed)
                     + f". You may want to give {person} a call.")
    if upcoming:
        parts.append("Still to come: " + ", ".join(f"{d['medication']} at {d['time']}" for d in upcoming) + ".")
    if not missed:
        parts.append("Everything is on track.")
    return " ".join(parts)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))  # http://localhost:8000/mcp
