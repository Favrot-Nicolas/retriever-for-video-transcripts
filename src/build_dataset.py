import logging
import random
import time
from pathlib import Path

from langchain_core.documents import Document
from pytube import Playlist
from youtube_transcript_api import YouTubeTranscriptApi

from cleaning import clean_transcript_and_extract_url
from utils import second_to_timestamp


def fetch_and_save_transcript(video_id: str, output_path: str = "data/transcript.txt"):
    """Fetches the transcript for a given YouTube video ID and saves it to a text file with timestamps."""
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id, languages=['fr'])

    lines = []
    url = "# https://www.youtube.com/watch/?v=" + video_id + "\n"
    current_line = ''
    current_start = None

    for snippet in transcript:
        if current_start is None:
            current_start = snippet.start

        current_line += " " + snippet.text

        if len(current_line) > 80:
            timestamp = second_to_timestamp(current_start)
            lines.append(f"{timestamp} {current_line.strip()}")
            current_line = ""
            current_start = None

    if current_line and current_start:
        timestamp = second_to_timestamp(current_start)
        lines.append(f"{timestamp} {current_line.strip()}")
    
    lines.insert(0, url)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def fetch_transcripts_from_playlist_id(
        playlist_id: str,
        output_folder: str = "data/api/"
    ):
    """Builds a dataset of transcripts from all videos in a YouTube playlist."""
    playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
    pl = Playlist(playlist_url)

    video_ids = [video.split("v=")[1].split("&")[0] for video in pl.video_urls]
    for video_index, video_id in enumerate(video_ids):
        logging.info(f"Fetching and saving transcript for video {video_id}...")
        output_path=f"{output_folder}/{pl.title}/{video_index}.txt"
        if Path(output_path).exists():
            logging.info(f"Transcript already exists at {output_path}, skipping...")
            continue
        fetch_and_save_transcript(video_id, output_path)
        sleep_time = 0.8+random.random()
        time.sleep(sleep_time)


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
    for path in sorted(folder.rglob("*.txt")):
        raw = path.read_text(encoding="utf-8", errors="ignore")
        cleaned, url = clean_transcript_and_extract_url(raw)
        if cleaned:
            metadata = {"source": path.name, "path": str(path)}
            if url:
                metadata["url"] = url
            docs.append(Document(page_content=cleaned, metadata=metadata))
    return docs