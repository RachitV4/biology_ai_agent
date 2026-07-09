import os
from pypdf import PdfReader
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
# Updated to the new, supported library
from langchain_chroma import Chroma

# 1. Load your API key
load_dotenv()

# 2. Initialize the embedding model
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

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
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def index_documents(chunks, filename):
    """Saves chunks into the persistent ChromaDB database using the latest library."""
    # This creates/connects to your local folder 'my_vector_db'
    vector_db = Chroma(
        persist_directory="./my_vector_db",
        embedding_function=embeddings,
        collection_name="biology_papers"
    )
    
    metadatas = [{"source": filename} for _ in chunks]
    vector_db.add_texts(texts=chunks, metadatas=metadatas)
    print(f"Stored {len(chunks)} chunks from {filename} into the database.")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # 1. Get all text from all PDFs
    papers = process_all_pdfs()
    
    # 2. Process, Chunk, AND Store each paper
    for paper in papers:
        chunks = chunk_text(paper['text'])
        index_documents(chunks, paper['filename'])
        
    print("\nAll documents have been indexed and saved to the database!")