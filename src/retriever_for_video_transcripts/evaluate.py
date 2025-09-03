import os

from langchain_community.vectorstores.faiss import FAISS

from retriever_for_video_transcripts.retrieve_timestamp import get_timestamp_for_chunk
from retriever_for_video_transcripts.urls import make_timed_url, timestamp_to_seconds


def evaluate_query(
        query:str,
        gt_source:str,
        gt_ts:str,
        vectorstore: FAISS,
        folder_path:str) -> dict:
    """
    Evaluate a single query:
    - query: the question string
    - gt_source: expected source filename (e.g. "s2-ep1.txt")
    - gt_ts: ground-truth timestamp string (e.g. "00:31:50.690")
    - vectorstore: your FAISS/Chroma index
    - folder_path: folder where the raw timestamped transcripts are stored
    """
    relevant_documents = vectorstore.similarity_search(query, k=1)
    retrieved = relevant_documents[0].page_content
    source = relevant_documents[0].metadata["source"]
    url = relevant_documents[0].metadata["url"]

    with open(os.path.join(folder_path, source), "r", encoding="utf-8") as f:
        timed_doc = f.read()

    pred_ts = get_timestamp_for_chunk(retrieved, timed_doc)

    ts_error = None
    if pred_ts is not None:
        ts_error = abs(timestamp_to_seconds(pred_ts) - timestamp_to_seconds(gt_ts))
        pred_url = make_timed_url(url, pred_ts)

    return {
        "question": query,
        "gt_source": gt_source,
        "pred_source": source,
        "source_correct": (source == gt_source),
        "gt_ts": gt_ts,
        "pred_ts": pred_ts,
        "ts_error_sec": ts_error,
        "pred_url": pred_url
    }
