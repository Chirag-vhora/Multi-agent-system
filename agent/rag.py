import os
from langchain_community.document_loaders import TextLoader
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

def get_vector_db():
    loader = TextLoader("vector_db/data/ai.txt")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    docs = splitter.split_documents(documents)

    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = "ai-agent"

    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )

    return PineconeVectorStore.from_documents(
        docs,
        embedding=get_embeddings(),
        index_name=index_name
    )

def get_retriever():
    global vector_db
    if vector_db is None:
        vector_db = get_vector_db()
    return vector_db.as_retriever()