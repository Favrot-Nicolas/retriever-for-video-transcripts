import dash_bootstrap_components as dbc

from dash import dash_table, dcc, html
from utils import list_txt_rows

video_holder = dcc.Loading(
        html.Div(
            html.Iframe(
                src=f"https://www.youtube.com/embed/",
                style={"width": "100%", "aspectRatio": "16/9"},
                id="video-iframe",
            ),
            style={"maxWidth": 600, "margin": "0 auto", "padding": 16}
            ),
        id="loading-overlay",
        type="default",  # or "circle", "dot", "cube"
        fullscreen=True,  # make it cover the whole page
)


transcripts_table = dash_table.DataTable(
    id="transcripts-table",
    columns=[
            {"name": "File Name", "id": "name", "deletable": False, "selectable": False},
            {"name": "path", "id": "path", "deletable": False, "selectable": False},
        ],
    data=list_txt_rows(), # type: ignore
    hidden_columns=["path"],
    editable=False,
    row_deletable=True,
    style_table={"overflowX": "auto"},
    style_cell={
            "minWidth": "140px",
            "maxWidth": "260px",
            "overflow": "hidden",
            "textOverflow": "ellipsis",
            "whiteSpace": "nowrap",
            "direction": "rtl",
            "textAlign": "center",
        }
)

introduction_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Video Transcript Retriever", className="card-title"),
                html.P(
                    "A tool to fetch, store, and retrieve video transcripts using LLMs.",
                    className="card-text",
                ),
            ]
        ),
    ],
    className="mt-3 mb-3",
)

search_bar = dbc.InputGroup(
    [
        dbc.Input(placeholder="What can I do for you ?", type="text", id="search-input"),
        dbc.Button("Search", color="primary", id="search-btn"),
    ],
    className="mb-3",
)

upload_bar = dbc.InputGroup(
    [
        dbc.Input(
            placeholder="Write a youtube playlist id to upload transcripts.",
            type="text", id="upload-input"),
        dbc.Button("Upload", color="primary", id="upload-btn"),
    ],
    className="mb-3",
)