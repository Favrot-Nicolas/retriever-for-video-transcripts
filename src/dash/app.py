# app.py
import logging
import os
from pathlib import Path

import dash_bootstrap_components as dbc
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

import dash
from build_dataset import fetch_transcripts_from_playlist_id
from dash import Input, Output, State, ctx, dcc, html
from evaluate import generate_url_from_query
from retrieve import embed_transcripts
from src.dash.components import (introduction_card, search_bar,
                                 transcripts_table, upload_bar, video_holder)
from utils import list_txt_rows

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

first_col = dbc.Col(
    [
        html.H5("Available Transcripts", className="mt-3"),
        transcripts_table
    ],
    width=3
)

second_col = dbc.Col(
    [
        introduction_card,
        upload_bar,
        search_bar,
        video_holder,
    ],
    width=9
)

app.layout = dbc.Container([
    dbc.Row([
        first_col,
        second_col,
    ]),
    dcc.Store(id="store-transcripts", data=[], storage_type="session"),
], fluid=True)


@app.callback(
    Output("transcripts-table", "data"),
    Input("upload-btn", "n_clicks"),
    Input("transcripts-table", "data"),
    State("upload-input", "value"),
    prevent_initial_call=True,
)
def refresh_table(_, updated_transcripts, playlist_id):
    trigger = ctx.triggered_id

    if trigger == "upload-btn" and playlist_id:
        output_folder=f"data/dash/{playlist_id}"
        os.makedirs(output_folder, exist_ok=True)
        logging.info(f"Fetching transcripts for playlist ID: {playlist_id}")
        fetch_transcripts_from_playlist_id(playlist_id, output_folder)
    
    elif trigger == "transcripts-table":
        old_transcripts = list_txt_rows()
        prev_paths = {row["path"] for row in (old_transcripts or [])}
        curr_paths = {row["path"] for row in (updated_transcripts or [])}
        deleted_paths = prev_paths - curr_paths
        logging.info(f"Deleted paths: {deleted_paths}")
        print(f"Deleted paths: {deleted_paths}")
        for path in deleted_paths:
            if Path(path).exists():
                os.remove(path)

    return list_txt_rows()

@app.callback(
    Output("video-iframe", "src"),
    Output("store-transcripts", "data"),
    Input("search-btn", "n_clicks"),
    State("search-input", "value"),
    State("store-transcripts", "data"),
    prevent_initial_call=True,
)
def update_video_holder(_, query, vs_transcripts_paths):
    if not query:
        return ""
    folder_path="data/dash"
    transcripts = list_txt_rows()
    paths = {row["path"] for row in (transcripts or [])}

    vs_path = f"data/vs"
    if (paths - set(vs_transcripts_paths)) or (set(vs_transcripts_paths) - paths):
        print("Transcripts have changed, re-embedding...")
        vectorstore = embed_transcripts(folder_path)
        vectorstore.save_local(vs_path)
        vs_transcripts_paths = list(paths)
    else:
        huggingface_embeddings = HuggingFaceEmbeddings(
            model_name="intfloat/multilingual-e5-large",
            model_kwargs={'device':'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        vectorstore = FAISS.load_local(
            vs_path,
            huggingface_embeddings,
            allow_dangerous_deserialization=True
        )
    
    url = generate_url_from_query(query, vectorstore, True)
    print(f"Generated URL: {url}")

    return url, vs_transcripts_paths

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
