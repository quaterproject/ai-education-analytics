from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
from langchain_cohere import CohereEmbeddings
from rich import print
embeddings = CohereEmbeddings(
    model="embed-english-v3.0",
)

# ! in memory vector store
# from langchain_core.vectorstores import InMemoryVectorStore

# embeddings = None
# vector_store = InMemoryVectorStore(embeddings)
# print("In-memory vector store created successfully." , vector_store)
# ! in memory vector store

# from langchain_chroma import Chroma

# vector_store = Chroma(
#     collection_name="example_collection",
#     embedding_function=embeddings,
#     persist_directory="../chroma_langchain_db",  # Where to save data locally, remove if not necessary
# )
# print("Chroma vector store created successfully." , vector_store)

# ! pinecone vector store for production use
# from langchain_pinecone import PineconeVectorStore
# from pinecone import Pinecone

# pc = Pinecone(api_key=...)
# index = pc.Index(index_name)

# vector_store = PineconeVectorStore(embedding=embeddings, index=index)

# ! use qdrant vector store working with all the vector store providers

from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

client = QdrantClient(":memory:")

# client = QdrantClient(path="./qdrant_data")

# client = QdrantClient(
#     url="https://your-cluster.cloud.qdrant.io",
#     api_key="YOUR_API_KEY",
# )

vector_size = len(embeddings.embed_query("sample text"))

if not client.collection_exists("test"):
    client.create_collection(
        collection_name="test",
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )
vector_store = QdrantVectorStore(
    client=client,
    collection_name="test",
    embedding=embeddings,
)

print("Qdrant vector store created successfully.", vector_store)

client.close()