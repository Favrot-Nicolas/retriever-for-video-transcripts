from pathlib import Path

from src.build_dataset import load_txt_folder_as_documents


def test_load_txt_folder_as_documents(tmp_path: Path):
    base = tmp_path / "data" / "dash" / "pl" / "Title"
    base.mkdir(parents=True)

    # with url and timestamps and noise
    (base / "0.txt").write_text(
        "# https://example.com/video\n"
        "00:00:00.000 Hello\n"
        "No text\n"
        "00:00:01.000 world!\n",
        encoding="utf-8",
    )

    # without url
    (base / "1.txt").write_text(
        "00:00:00 start\n00:00:01 end\n",
        encoding="utf-8",
    )

    docs = load_txt_folder_as_documents(tmp_path / "data" / "dash")
    assert len(docs) == 2

    d0 = next(d for d in docs if d.metadata["source"] == "0.txt")
    assert d0.metadata["url"] == "https://example.com/video"
    assert d0.page_content == "Hello world!"

    d1 = next(d for d in docs if d.metadata["source"] == "1.txt")
    assert "url" not in d1.metadata
    assert d1.page_content == "start end"


