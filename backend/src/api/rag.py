import os
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_cohere import CohereEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import sys

# Ensure config can be imported from root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from config import BASE_URL, API_KEY, MODEL

load_dotenv()

# Initialize Qdrant Client
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "asset_compliance"

client = None
vector_store = None
embeddings = CohereEmbeddings(model="embed-english-v3.0")

if QDRANT_URL and QDRANT_API_KEY:
    try:
        client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        # Check if collection exists
        if not client.collection_exists(COLLECTION_NAME):
            # Cohere english-v3.0 yields 1024 dimensions
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
            )
        vector_store = QdrantVectorStore(
            client=client,
            collection_name=COLLECTION_NAME,
            embedding=embeddings
        )
        print("Connected to Qdrant Cloud collection:", COLLECTION_NAME)
    except Exception as e:
        print(f"Error initializing Qdrant Cloud: {e}. Falling back to in-memory Qdrant Client.")
        client = QdrantClient(":memory:")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
        )
        vector_store = QdrantVectorStore(
            client=client,
            collection_name=COLLECTION_NAME,
            embedding=embeddings
        )
else:
    print("No Qdrant config found in env. Initializing in-memory Qdrant.")
    client = QdrantClient(":memory:")
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
    )
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings
    )

llm = ChatOpenAI(
    model=MODEL,
    api_key=API_KEY,
    base_url=BASE_URL,
    temperature=0.2
)

def index_document(file_path: str):
    """
    Parses a PDF or Text file, chunks it, and uploads to Qdrant.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    print(f"Indexing document: {file_path}")
    
    docs = []
    if file_path.lower().endswith(".pdf"):
        loader = PyPDFLoader(file_path)
        docs = loader.load()
    else:
        # Load as raw text file
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        from langchain_core.documents import Document
        docs = [Document(page_content=text, metadata={"source": file_path})]
        
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)
    
    if chunks:
        vector_store.add_documents(chunks)
        print(f"Successfully added {len(chunks)} chunks to Qdrant.")
    return len(chunks)

def query_compliance_docs(query_text: str, k=3):
    """
    Performs similarity search in Qdrant for the query.
    """
    try:
        results = vector_store.similarity_search(query_text, k=k)
        return "\n\n".join([r.page_content for r in results])
    except Exception as e:
        print("Error during similarity search:", e)
        return ""

def generate_report(asset_name, location, lstm_class, lstm_importance, cnn_class, cnn_conf, ann_class, query=None):
    """
    Queries relevant guidelines using RAG and generates a structured risk assessment report.
    """
    # 1. Fetch relevant guidelines from Qdrant
    rag_query = f"structural safety regulations, maintenance guidelines for {asset_name} with risk class {lstm_class}"
    context = query_compliance_docs(rag_query, k=2)
    
    if not context:
        context = "No specific regulation docs found. Use general engineering and asset safety standards."

    # Map classifications
    lstm_mapping = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}
    cnn_mapping = {0: "Healthy (No visible cracks)", 1: "Damaged (Cracks/Scratches detected)"}
    ann_mapping = {0: "Normal machine sound", 1: "Anomalous operation sound detected"}
    
    lstm_status = lstm_mapping.get(lstm_class, "Unknown")
    cnn_status = cnn_mapping.get(cnn_class, "Unknown")
    ann_status = ann_mapping.get(ann_class, "Unknown")
    
    # Format model predictions for prompt
    input_details = f"""
Asset Name: {asset_name}
Location: {location}

Model Diagnostic Output:
- Time-Series Tabular Risk (LSTM): {lstm_status}
- Tabular Feature Importance: {lstm_importance}
- Visual Inspection Status (CNN): {cnn_status} (CNN confidence: {cnn_conf:.2f})
- Machine Sound Diagnostic (ANN): {ann_status}
"""

    prompt = f"""You are a senior asset inspector and risk analyst. You must write an official evaluation report based on the following diagnostic results and retrieved compliance guidelines.

RETRIVED COMPLIANCE GUIDELINES:
{context}

DIAGNOSTIC RESULTS:
{input_details}

Generate a report formatted strictly using the following tags:
<summary>
Write a concise 2-3 sentence executive summary of the asset's health status and overall risk level.
</summary>
<reasoning>
Explain the technical reasoning behind the findings. Combine the LSTM time-series results (referencing feature importances like temperature or vibration anomalies), CNN image cracks detection, and audio anomaly.
</reasoning>
<mitigation>
Propose 3 action steps / mitigation strategies to repair or maintain this asset in compliance with regulations.
</mitigation>

Make the report detailed and professional. Output only the tagged segments.
"""
    
    response = llm.invoke(prompt)
    content = response.content
    
    # Parse tags
    summary = extract_tag(content, "summary")
    reasoning = extract_tag(content, "reasoning")
    mitigation = extract_tag(content, "mitigation")
    
    return {
        "summary": summary,
        "reasoning": reasoning,
        "mitigation": mitigation
    }

def extract_tag(text, tag_name):
    pattern = f"<{tag_name}>(.*?)</{tag_name}>"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Fallback if tags are missing or capitalized
    pattern_icase = f"<{tag_name}>(.*?)</{tag_name}>"
    match_icase = re.search(pattern_icase, text, re.DOTALL | re.IGNORECASE)
    if match_icase:
        return match_icase.group(1).strip()
    return text.strip()
