import re
from datetime import timedelta
from pathlib import Path


def timestamp_to_seconds(ts: str) -> int:
    """
    Convert 'HH:MM:SS.xxx' or 'MM:SS.xxx' to total seconds (int).
    """
    parts = ts.split(":")
    parts = [p.split(".")[0] for p in parts]
    parts = list(map(int, parts))
    if len(parts) == 3:
        h, m, s = parts
    elif len(parts) == 2:
        h, m, s = 0, *parts
    else:
        raise ValueError(f"Unrecognized timestamp format: {ts}")
    return h * 3600 + m * 60 + s


def second_to_timestamp(seconds: float) -> str:
    """
    Convert seconds to HH:MM:SS.mmm
    """
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    millis = int(td.microseconds / 1000)
    return f"{hours:02}:{minutes:02}:{secs:02}.{millis:03}"


def extract_number_from_name(name: str) -> int:
    """Extract the last integer from something like 'folder/15.txt'"""
    match = re.search(r"(\d+)(?=\.txt$)", name)
    return int(match.group(1)) if match else -1

def list_txt_rows(data_dir: Path = Path("data/dash")) -> list[dict[str, str]]:
    """List all .txt files in the given directory and its subdirectories.
        Returns a list of dicts with 'name' and 'path' keys,
        sorted by the number in the filename.
    Args:
        data_dir (Path): Path to the directory to search. Defaults to 'data/dash'.
    Returns:
        list[dict[str, str]]: List of dicts with 'name' and 'path' keys.
    """
    rows = []
    for p in data_dir.rglob("*.txt"):
        rows.append({
            "name": f"{p.parent.name}/{p.name}",
            "path": str(p.resolve()),
        })
    return sorted(rows, key=lambda r: extract_number_from_name(r["name"]))