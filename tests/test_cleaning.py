from src.cleaning import clean_transcript_and_extract_url


def test_clean_transcript_and_extract_url_basic():
    raw = (
        "# https://www.youtube.com/watch?v=dQw4w9WgXcQ\n"
        "00:00:00.000 Hello there\n"
        "00:00:01.000 General Kenobi\n"
        "# header\n"
        "00:00:02.000 \n"
        "No text\n"
        "00:00:03.000 end.\n"
    )
    cleaned, url = clean_transcript_and_extract_url(raw)
    assert url == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert cleaned == "Hello there General Kenobi end."


def test_clean_transcript_handles_no_url():
    raw = (
        "00:00:00 start\n"
        "00:00:01 middle\n"
        "00:00:02 end\n"
    )
    cleaned, url = clean_transcript_and_extract_url(raw)
    assert url is None
    assert cleaned == "start middle end"


