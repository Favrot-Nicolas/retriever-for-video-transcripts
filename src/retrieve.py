from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from build_dataset import load_txt_folder_as_documents


def embed_transcripts(folder_path: str) -> FAISS:
    """Embed all transcripts in a folder and return a FAISS vectorstore.
    Args:
        folder_path (str): Path to folder with .txt files
    Returns:
        FAISS: FAISS vectorstore with embedded transcripts
    """
    
    docs_before_split = load_txt_folder_as_documents(folder_path)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 700,
        chunk_overlap  = 50,
    )
    docs_after_split = text_splitter.split_documents(docs_before_split)

    huggingface_embeddings = HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-large",
        model_kwargs={'device':'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    vectorstore = FAISS.from_documents(docs_after_split, huggingface_embeddings)
    return vectorstore