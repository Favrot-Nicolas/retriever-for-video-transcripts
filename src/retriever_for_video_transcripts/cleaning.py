import re
from pathlib import Path

from langchain_core.documents import Document

TIMESTAMP_RE = re.compile(r"^\s*\d{2}:\d{2}:\d{2}(?:[.,]\d{3})?\s*")
URL_RE = re.compile(r"^#?\s*https?://\S+")

def clean_transcript_and_extract_url(text: str) -> tuple[str, str | None]:
    """Clean a raw transcript text:
    - Remove timestamps at start of lines
    - Remove comment-style headers (lines starting with #)
    - Remove empty lines and lines with "No text"
    - Extract first URL found (line starting with http(s)://)   

    Args:
        text (str): Raw transcript text

    Returns:
        tuple[str, str | None]: Cleaned text and extracted URL (or None if not found)
    """
    cleaned_lines = []
    url = None

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        # capture and skip url
        if URL_RE.match(line):
            if url is None:
                url = line.lstrip("#").strip()
            continue

        # skip comment-style headers
        if line.startswith("#"):
            continue

        # remove leading timestamp if present
        line = TIMESTAMP_RE.sub("", line)

        # skip useless lines
        if not line.strip():
            continue
        if line.strip().lower() == "no text":
            continue

        cleaned_lines.append(line)

    merged = " ".join(cleaned_lines)
    merged = re.sub(r"\s+", " ", merged).strip()
    return merged, url

def load_txt_folder_as_documents(folder: str | Path) -> list[Document]:
    """Load transcript text files from a folder, clean them, 
    and return as list of langchain Documents.

    Args:
        folder (str | Path): Path to folder with .txt files

    Returns:
        list[Document]: List of cleaned Documents with metadata
    """
    folder = Path(folder)
    docs: list[Document] = []
    for path in sorted(folder.glob("*.txt")):
        raw = path.read_text(encoding="utf-8", errors="ignore")
        cleaned, url = clean_transcript_and_extract_url(raw)
        if cleaned:
            metadata = {"source": path.name, "path": str(path)}
            if url:
                metadata["url"] = url
            docs.append(Document(page_content=cleaned, metadata=metadata))
    return docs