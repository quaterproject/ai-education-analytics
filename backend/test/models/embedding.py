from langchain_cohere import CohereEmbeddings

from langchain_core.vectorstores import InMemoryVectorStore
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
from rich import print
from langchain.embeddings import init_embeddings

embeddings = CohereEmbeddings(
    model="embed-english-v3.0",
)

embeddings2 = init_embeddings(
    model="embed-english-v3.0",
    provider="cohere",
)

# Create a vector store with a sample text

text = "LangChain is the framework for building context-aware reasoning applications"

vectorstore = InMemoryVectorStore.from_texts(
    [text],
    embedding=embeddings2,
)

# Use the vectorstore as a retriever
retriever = vectorstore.as_retriever()

# Retrieve the most similar text
retrieved_documents = retriever.invoke("What is LangChain?")

# show the retrieved document's content
res = retrieved_documents[0].page_content
print(res)