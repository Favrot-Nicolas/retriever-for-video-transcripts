import re
import unicodedata
from difflib import SequenceMatcher
from typing import List, Optional, Tuple

TIMESTAMP_LINE_RE = re.compile(
    r"^\s*(\d{2}:\d{2}:\d{2}(?:[.,]\d{3})?)\s+(.*\S)\s*$"
)

def _strip_accents(s: str) -> str:
    """Strip accents from input string."""
    return "".join(
        ch for ch in unicodedata.normalize("NFKD", s)
        if not unicodedata.combining(ch)
    )

def _normalize(s: str) -> str:
    """Lowercase, strip accents, normalize whitespace and quotes."""
    s = s.lower()
    s = _strip_accents(s)
    s = s.replace("’", "'")
    s = re.sub(r"\s+", " ", s).strip()
    return s

def _first_sentence(text: str) -> str:
    """Return the first sentence or first 20 words, whichever is shorter."""
    m = re.search(r"[\.!?…]+", text)
    if m and m.end() > 10:
        sent = text[:m.end()]
    else:
        words = text.strip().split()
        sent = " ".join(words[:20]) if len(words) > 20 else " ".join(words)
    return sent.strip()

def _parse_timed_transcript(doc: str) -> List[Tuple[str, str]]:
    """Parse a timestamped transcript into (timestamp, text) pairs. 
    Lines without timestamps are ignored.
    Returns list of (timestamp, text) tuples.
    """
    pairs = []
    for line in doc.splitlines():
        m = TIMESTAMP_LINE_RE.match(line)
        if not m:
            continue
        ts, content = m.group(1), m.group(2)
        if content.strip():
            pairs.append((ts, content))
    return pairs

def _build_corpus(pairs: List[Tuple[str, str]]):
    """
    Build a normalized corpus and an index that maps character spans to timestamps.
    Returns (corpus_string, spans) where spans = [(start, end, ts), ...]
    """
    pieces = []
    spans = []
    cursor = 0
    for ts, txt in pairs:
        norm = _normalize(txt)
        if not norm:
            continue
        start = cursor
        pieces.append(norm)
        cursor += len(norm)
        spans.append((start, cursor, ts))
        pieces.append(" ")
        cursor += 1
    corpus = "".join(pieces).strip()

    if corpus and pieces and pieces[-1] == " ":
        corpus = corpus[:-1]
        if spans:
            s0, e0, ts0 = spans[-1]
            spans[-1] = (s0, e0 - 1, ts0)
    return corpus, spans

def _timestamp_for_index(spans: List[Tuple[int, int, str]], idx: int) -> Optional[str]:
    """
    Map a character index in the corpus to the corresponding line's timestamp.
    """
    for start, end, ts in spans:
        if start <= idx < end:
            return ts

def get_timestamp_for_chunk(retrieved_chunk: str, timed_transcript_text: str) -> Optional[str]:
    """
    Return the timestamp (e.g. '00:12:51.030') for where the FIRST SENTENCE
    of the retrieved chunk begins in the timestamped transcript.
    """
    pairs = _parse_timed_transcript(timed_transcript_text)
    if not pairs:
        return None

    corpus, spans = _build_corpus(pairs)

    first_sent = _first_sentence(retrieved_chunk)
    query = _normalize(first_sent)

    if not query or not corpus:
        return None

    # 1) Exact substring search on normalized text
    pos = corpus.find(query)
    if pos != -1:
        return _timestamp_for_index(spans, pos)

    # 2) Try a shorter prefix (first 12–18 words) to handle small mismatches
    words = query.split()
    if len(words) > 18:
        prefix = " ".join(words[:18])
        pos2 = corpus.find(prefix)
        if pos2 != -1:
            return _timestamp_for_index(spans, pos2)

    if len(words) > 12:
        prefix = " ".join(words[:12])
        pos3 = corpus.find(prefix)
        if pos3 != -1:
            return _timestamp_for_index(spans, pos3)

    # 3) Light fuzzy backup: longest common match location
    sm = SequenceMatcher(None, corpus, query, autojunk=False)
    match = sm.find_longest_match(0, len(corpus), 0, len(query))
    coverage = match.size / max(1, len(query))
    if coverage >= 0.6:
        return _timestamp_for_index(spans, match.a)

    return None


def test():
    return None
