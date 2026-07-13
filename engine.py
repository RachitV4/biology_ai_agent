import os
import tempfile
from pathlib import Path
from pypdf import PdfReader
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Initialize local models
embeddings = OllamaEmbeddings(model="nomic-embed-text")
llm = ChatOllama(model="qwen3:14b")

def process_and_index_pdfs(directory_path, session_id):
    vector_db = Chroma(persist_directory="./my_vector_db", embedding_function=embeddings, collection_name=session_id)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
    
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            path = os.path.join(directory_path, filename)
            try:
                reader = PdfReader(path)
                full_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
                chunks = text_splitter.create_documents([full_text], metadatas=[{"source": filename}])
                vector_db.add_documents(chunks)
            except Exception as e:
                print(f"Error indexing {filename}: {e}")
    return f"Indexed {len(os.listdir(directory_path))} papers into session: {session_id}"

def process_and_index_pdfs_temporary(uploaded_files, session_id):
    with tempfile.TemporaryDirectory() as temp_dir:
        for uploaded_file in uploaded_files:
            temp_path = Path(temp_dir) / uploaded_file.name
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        return process_and_index_pdfs(temp_dir, session_id)

def ask_agent(query, session_id):
    vector_db = Chroma(persist_directory="./my_vector_db", embedding_function=embeddings, collection_name=session_id)
    
    # Updated to k=10 for broader cross-document context
    docs = vector_db.similarity_search(query, k=10)
    if not docs:
        return "I couldn't find relevant information in the uploaded papers."
        
    context_text = "\n\n".join([f"Source: {doc.metadata.get('source')}\nContent: {doc.page_content}" for doc in docs])
    
    prompt = f"""
    You are an expert biology research assistant. 
    Use the provided research context to answer the question.
    Cite the Source name for every claim you make.
    
    Context:
    {context_text}
    
    Question: 
    {query}
    """
    return llm.invoke(prompt).content

def synthesize_research(session_id):
    """Generates a summary report across all indexed papers."""
    vector_db = Chroma(persist_directory="./my_vector_db", embedding_function=embeddings, collection_name=session_id)
    
    # Fetch all documents in the collection
    docs = vector_db.get()
    if not docs['documents']:
        return "No documents indexed yet."
        
    context_text = "\n\n".join([f"Source: {d.get('source')}\nContent: {c}" for d, c in zip(docs['metadatas'], docs['documents'])])
    
    prompt = f"""
    You are a Senior Biology Research Analyst. 
    Analyze the following research papers and provide a professional synthesis report.
    Structure your report into:
    1. Common Themes across all papers.
    2. Key Methodological Differences.
    3. Any conflicting findings between the sources.
    
    Context:
    {context_text}
    """
    return llm.invoke(prompt).content