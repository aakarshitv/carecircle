import os
import tempfile

os.environ["CARECIRCLE_DB"] = tempfile.mktemp(suffix=".db")

import server  # noqa: E402


def test_taken_missed_upcoming():
    server.add_medication("Dad", "Amlodipine", "5mg", ["08:00", "20:00"])
    server.add_medication("Dad", "Metformin", "500mg", ["13:00"])
    assert "08:00" in server.log_dose("Dad", "amlodipine", now="2026-10-23T08:20")
    assert "couldn't find" in server.log_dose("Dad", "aspirin", now="2026-10-23T08:20")

    doses = server.check_status("Dad", now="2026-10-23T16:00")["doses"]
    assert [(d["medication"], d["time"], d["status"]) for d in doses] == [
        ("amlodipine", "08:00", "taken"),
        ("metformin", "13:00", "missed"),
        ("amlodipine", "20:00", "upcoming"),
    ]
    summary = server.daily_summary("Dad", now="2026-10-23T16:00")
    assert "1 of 3" in summary and "metformin at 13:00" in summary
    assert "No medications" in server.daily_summary("Mom")
