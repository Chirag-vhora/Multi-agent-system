import os

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings


def upload_to_vector_db(file_path: str):

    ext = file_path.split(".")[-1].lower()

    # Load file
    if ext == "txt":
        loader = TextLoader(file_path)

    elif ext == "pdf":
        loader = PyPDFLoader(file_path)

    else:
        return "Unsupported file"

    docs = loader.load()

    # Split text
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(docs)

    # Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Pinecone
    pc = Pinecone(
        api_key=os.getenv("PINECONE_API_KEY")
    )

    index_name = "ai-agent"

    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

    PineconeVectorStore.from_documents(
        chunks,
        embedding=embeddings,
        index_name=index_name,
        namespace="uploaded-docs"
    )

    return "Upload Success"