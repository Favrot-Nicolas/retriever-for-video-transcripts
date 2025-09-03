from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


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

def make_timed_url(base_url: str, ts: str) -> str:
    """
    Return a YouTube (or similar) URL with the start time param.
    """
    seconds = timestamp_to_seconds(ts)

    url = base_url.strip()

    if "youtube.com" in url:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        query["t"] = [str(seconds)]
        new_query = urlencode(query, doseq=True)
        new_url = urlunparse(parsed._replace(query=new_query))
        return new_url
    else:
        return f"{url}#t={seconds}s"
