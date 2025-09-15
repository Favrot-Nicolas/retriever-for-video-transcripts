import os
from pathlib import Path

from src.utils import (extract_number_from_name, list_txt_rows,
                       second_to_timestamp, timestamp_to_seconds)


def test_timestamp_to_seconds_roundtrip():
    assert timestamp_to_seconds("00:00:05.123") == 5
    assert timestamp_to_seconds("01:02:03.999") == 3723
    assert timestamp_to_seconds("02:03") == 123

    # roundtrip with integer seconds
    for secs in [0, 5, 59, 60, 61, 3723]:
        ts = second_to_timestamp(secs)
        assert timestamp_to_seconds(ts) == secs


def test_extract_number_from_name():
    assert extract_number_from_name("folder/15.txt") == 15
    assert extract_number_from_name("15.txt") == 15
    assert extract_number_from_name("folder/no-num.txt") == -1


def test_list_txt_rows(tmp_path: Path, monkeypatch):
    # create nested structure
    base = tmp_path / "data" / "dash" / "pl" / "Title"
    base.mkdir(parents=True)
    for i in [0, 2, 1]:
        (base / f"{i}.txt").write_text(f"#{i}", encoding="utf-8")

    # ensure function points to tmp data dir
    rows = list_txt_rows(tmp_path / "data" / "dash")
    assert [r["name"] for r in rows] == ["Title/0.txt", "Title/1.txt", "Title/2.txt"]
    assert all(Path(r["path"]).exists() for r in rows)


