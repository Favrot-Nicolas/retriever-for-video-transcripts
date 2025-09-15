### retriever-for-video-transcripts

Build a small RAG over YouTube video transcripts. Given a natural-language query, it retrieves the most relevant video moment and returns a YouTube URL with timestamp.

### Features
- **Transcript ingestion**: Fetch transcripts from a YouTube playlist and save them as timestamped `.txt` files.
- **Embeddings + Vector store**: Chunk transcripts and embed with `intfloat/multilingual-e5-large` into a local FAISS index.
- **Simple UI**: Dash app to upload playlist IDs, manage transcripts, search, and open the best timestamped URL.
- **Notebooks**: Minimal demos for experimentation.

### Requirements
- Python 3.10+
- macOS/Linux/Windows
- Internet access for model and transcript downloads

### Installation

Using requirements.txt (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

Using Poetry (optional):
```bash
curl -sSL https://install.python-poetry.org | python3 -
poetry env use 3.10
poetry install --no-root
# Populate runtime deps from requirements.txt inside the Poetry venv
poetry run pip install -r requirements.txt
```

### Project layout
```text
src/
  build_dataset.py       # fetch/save transcripts, load as LangChain Documents
  retrieve.py            # embed transcripts and build FAISS
  dash/app.py            # Dash UI (upload, list, search, open URL)
  dash/components.py     # UI components
  utils.py, cleaning.py  # helpers
data/
  dash/                  # transcripts stored by playlist/title/index.txt
  vs/                    # FAISS index (index.faiss / index.pkl)
notebooks/               # demo notebooks
```

### Quick start

1) Prepare environment (Poetry or pip as above).

2) Run the Dash app:
```bash
python src/dash/app.py
```
Then open the printed local URL (typically `http://127.0.0.1:8050`).

3) In the UI:
- Paste a YouTube playlist ID and click Upload to fetch transcripts to `data/dash/<playlist>/<Title>/*.txt`.
- Click Search after entering a query. The app embeds transcripts (or reloads the saved FAISS index from `data/vs/`) and opens the best YouTube URL with timestamp in the iframe.

The app automatically re-embeds when it detects transcripts have changed.

### Programmatic usage

Embed all transcripts under a folder and persist FAISS:
```python
from src.retrieve import embed_transcripts

vectorstore = embed_transcripts("data/dash")
vectorstore.save_local("data/vs")
```

Fetch transcripts from a playlist (saved under `data/dash/<playlist>/<Title>/index.txt`):
```python
from src.build_dataset import fetch_transcripts_from_playlist_id

fetch_transcripts_from_playlist_id("<PLAYLIST_ID>", "data/dash/<PLAYLIST_ID>")
```

### Notebooks
- `notebooks/1_demo.ipynb` and `notebooks/2_simple_retriever.ipynb` show simple ingestion and retrieval flows. Launch with your preferred Jupyter environment after installing dependencies.

### Testing and linting
```bash
pytest -q
ruff check .
```
Optionally enable pre-commit hooks:
```bash
pre-commit install
```

### Troubleshooting
- **Model downloads slow/large**: The embedding model `intfloat/multilingual-e5-large` will download on first use. Ensure enough disk space and a stable connection.
- **FAISS load errors**: Use `faiss-cpu` for portability. If you switch Python versions, rebuild the index.
- **YouTube transcript errors**: Some videos lack transcripts or rate limits apply. The code waits ~1s between requests; you can adjust in `fetch_transcripts_from_playlist_id`.
- **M1/M2 macOS**: Running on CPU works out of the box. If you want GPU acceleration, follow platform-specific instructions for PyTorch/Transformers.

### License
MIT © 2024-present Nicolas Favrot