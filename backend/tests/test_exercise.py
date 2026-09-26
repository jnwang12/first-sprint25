"""Phase 1 checks use offline data, never live credentials."""
import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from backend import exercise


def test_prints_tuples_with_explicit_field_order_and_duplicate_names(monkeypatch, capsys):
    records = json.loads(
        (Path(__file__).parents[1] / "fixtures/phase1_students.json").read_text()
    )
    client = Mock()
    client.table.return_value.select.return_value.execute.return_value.data = records
    monkeypatch.setattr(exercise, "get_supabase_client", lambda: client)

    exercise.main()

    assert capsys.readouterr().out.splitlines() == [
        "('Prad', 'practice.prad.cs@example.com', 'Computer Science')",
        "('Maya Chen', 'practice.maya@example.com', 'Mechanical Engineering')",
        "('Prad', 'practice.prad.math@example.com', 'Mathematics')",
    ]


def test_empty_result_has_feedback(monkeypatch, capsys):
    client = Mock()
    client.table.return_value.select.return_value.execute.return_value.data = []
    monkeypatch.setattr(exercise, "get_supabase_client", lambda: client)

    exercise.main()

    assert "No student records are visible" in capsys.readouterr().out


def test_query_failure_is_not_reported_as_empty(monkeypatch, capsys):
    client = Mock()
    client.table.return_value.select.return_value.execute.side_effect = RuntimeError("Read failed")
    monkeypatch.setattr(exercise, "get_supabase_client", lambda: client)

    with pytest.raises(RuntimeError, match="Read failed"):
        exercise.main()
    assert capsys.readouterr().out == ""
