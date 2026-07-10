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
    """Reads PDFs, chunks them, and stores in ChromaDB."""
    vector_db = Chroma(
        persist_directory="./my_vector_db", 
        embedding_function=embeddings, 
        collection_name=session_id
    )
    
    # Semantic splitter for biology context preservation
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
        add_start_index=True
    )
    
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
    
    return f"Indexed into session: {session_id}"

def process_and_index_pdfs_temporary(uploaded_files, session_id):
    """
    Saves uploaded web files to a temporary directory 
    then triggers the indexer so no permanent files are left on disk.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        for uploaded_file in uploaded_files:
            temp_path = Path(temp_dir) / uploaded_file.name
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        return process_and_index_pdfs(temp_dir, session_id)

def ask_agent(query, session_id):
    vector_db = Chroma(
        persist_directory="./my_vector_db", 
        embedding_function=embeddings, 
        collection_name=session_id
    )
    
    # Retrieve the 4 most relevant chunks
    docs = vector_db.similarity_search(query, k=4)
    if not docs:
        return "I couldn't find relevant information in the uploaded papers."
        
    # Create a string with context and track sources
    context_text = ""
    sources = set()
    for doc in docs:
        context_text += f"\n\nSource: {doc.metadata.get('source', 'Unknown')}\nContent: {doc.page_content}"
        sources.add(doc.metadata.get('source', 'Unknown'))
    
    # Prompt the LLM to include citations
   # Update the prompt inside ask_agent in engine.py
    prompt = f"""
    You are an expert biology research assistant. 
    Use the provided research context to answer the question.
    Cite the sources provided in the context (e.g., use the filename provided in the 'Source' tag).
    
    Context:
    {context_text}
    
    Question: 
    {query}
    """
    
    
    response = llm.invoke(prompt)
    return response.content