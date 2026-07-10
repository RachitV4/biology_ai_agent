import os
from pypdf import PdfReader
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# 1. Initialize local models
# We use 'nomic-embed-text' for embedding and your local qwen3:14b for the LLM later
embeddings = OllamaEmbeddings(model="nomic-embed-text")

def extract_text_from_pdf(pdf_path):
    """Reads a single PDF and returns its text."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def process_all_pdfs(directory_path="data/"):
    """Scans the 'data/' folder and extracts text from every PDF found."""
    all_data = []
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' not found!")
        return all_data

    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            print(f"Processing: {filename}...")
            path = os.path.join(directory_path, filename)
            try:
                text = extract_text_from_pdf(path)
                all_data.append({"filename": filename, "text": text})
            except Exception as e:
                print(f"Could not read {filename}: {e}")
    return all_data

def chunk_text(text, chunk_size=1000):
    """Splits a long string into smaller, manageable chunks."""
    # Note: In production, consider RecursiveCharacterTextSplitter for better quality
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def index_documents(chunks, filename, session_id):
    """Saves chunks into the local ChromaDB database."""
    # Using the session_id as the collection name isolates the user's papers
    vector_db = Chroma(
        persist_directory="./my_vector_db",
        embedding_function=embeddings,
        collection_name=session_id
    )
    
    metadatas = [{"source": filename} for _ in chunks]
    vector_db.add_texts(texts=chunks, metadatas=metadatas)
    print(f"Stored {len(chunks)} chunks from {filename} into collection '{session_id}'.")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # This session_id will eventually come from your website
    current_session = "biology_research_session_001"
    
    # 1. Get all text from all PDFs
    papers = process_all_pdfs()
    
    # 2. Process, Chunk, AND Store each paper
    for paper in papers:
        chunks = chunk_text(paper['text'])
        index_documents(chunks, paper['filename'], current_session)
        
    print(f"\nAll documents have been indexed to session: {current_session}")