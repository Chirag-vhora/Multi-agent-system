import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings

vector_db = None
embeddings = None

def get_embeddings():
    global embeddings
    if embeddings is None:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    return embeddings

def get_pinecone_store(namespace="uploaded-docs"):
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = "ai-agent"

    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )

    return PineconeVectorStore(
        index_name=index_name,
        embedding=get_embeddings(),
        namespace=namespace
    )

def upload_to_vector_db(file_path: str):
    ext = file_path.split(".")[-1].lower()

    if ext == "txt":
        loader = TextLoader(file_path)
    elif ext == "pdf":
        loader = PyPDFLoader(file_path)
    else:
        return "Unsupported file"

    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(docs)

    store = get_pinecone_store("uploaded-docs")
    store.add_documents(chunks)

    global vector_db
    vector_db = store

    return "Upload Success"

def get_retriever():
    global vector_db
    if vector_db is None:
        vector_db = get_pinecone_store("uploaded-docs")

    return vector_db.as_retriever()