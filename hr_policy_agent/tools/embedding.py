import os
import pdfplumber
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
# CORRECT IMPORT FOR 2025
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Configuration
PERSIST_DIR = "/Users/bootlabs/Downloads/hr-policy-assistance/hr_policy_agent/chroma_db"
# Use a valid Gemini embedding model name
EMBED_MODEL = "models/gemini-embedding-001"

async def ingest_local_documents():
    """
    Scans for PDFs, extracts text, chunks it, and stores in Chroma.
    """
    local_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    print(local_files)
    if not local_files:
        return "No PDF files found."

    all_text_chunks = []
    all_metadatas = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    for filename in local_files:
        try:
            with pdfplumber.open(filename) as pdf:
                full_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
                chunks = text_splitter.split_text(full_text)
                print(chunks)
                all_text_chunks.extend(chunks)
                all_metadatas.extend([{"source": filename} for _ in chunks])
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

    if not all_text_chunks:
        return "Extraction failed."

    # Use the correct generative embedding class
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBED_MODEL)

    vectorstore = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )

    vectorstore.add_texts(texts=all_text_chunks, metadatas=all_metadatas)
    return f"Success: Ingested {len(all_text_chunks)} chunks."

async def query_local_docs(query_text: str):
    """
    Retrieves context from the local vector database.
    """
    # Fixed: Use GoogleGenerativeAIEmbeddings instead of GeminiEmbeddings
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBED_MODEL)

    vectorstore = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    relevant_docs = retriever.invoke(query_text)

    if not relevant_docs:
        return "No relevant information found."

    return "\n---\n".join([doc.page_content for doc in relevant_docs])
