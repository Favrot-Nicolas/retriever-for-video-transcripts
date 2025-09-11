from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from utils import timestamp_to_seconds


def make_timed_url(base_url: str, ts: str, embed: bool = False) -> str:
    """
    Return a YouTube (or similar) URL with the start time param.

    Args:
        base_url: YouTube or other video URL
        ts: timestamp string like '00:19:58.260'
        embed: if True, return embed URL format with ?start=SECONDS
    """
    seconds = timestamp_to_seconds(ts)
    url = base_url.strip()
    parsed = urlparse(url)

    if "youtube.com" in url:
        query = parse_qs(parsed.query)
        video_id = query.get("v", [None])[0]

        if embed and video_id:
            return f"https://www.youtube.com/embed/{video_id}?start={seconds}"
        else:
            query["t"] = [str(seconds)]
            new_query = urlencode(query, doseq=True)
            return urlunparse(parsed._replace(query=new_query))

    return f"{url}#t={seconds}s"
