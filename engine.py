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
    vector_db = Chroma(persist_directory="./my_vector_db", embedding_function=embeddings, collection_name=session_id)
    docs = vector_db.get()
    if not docs['documents']:
        return "No documents indexed yet."
        
    context_text = "\n\n".join([f"SOURCE_FILE: {d.get('source')}\nCONTENT: {c}" for d, c in zip(docs['metadatas'], docs['documents'])])
    
    prompt = f"""
    You are a Senior Biology Research Analyst. 
    Analyze the following research context.
    
    CRITICAL INSTRUCTION: You must group your analysis by the 'SOURCE_FILE' tag. Do not summarize themes globally until you have first analyzed every file individually.
    
    Structure your report into:
    1. Analysis per Document: For every unique 'SOURCE_FILE' found in the context, create a dedicated subsection. 
       State the name of the file and list its top 3 key technical ideas/findings clearly.
    2. Cross-Document Synthesis: Discuss common themes and conflicting findings across these papers.
    3. Notable Researchers & Contributions: Identify the key authors and their focus.
    4. Technical Challenges: Summarize the main obstacles identified.
    
    Context:
    {context_text}
    """
    return llm.invoke(prompt).content
   