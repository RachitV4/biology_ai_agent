import os
from pypdf import PdfReader
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Initialize your local AI "Brain" and "Map" models
# These assume you have 'nomic-embed-text' and 'qwen3:14b' pulled in Ollama
embeddings = OllamaEmbeddings(model="nomic-embed-text")
llm = ChatOllama(model="qwen3:14b")

def process_and_index_pdfs(directory_path, session_id):
    """
    Reads all PDFs, breaks them into semantic chunks that preserve 
    biological context, and saves them to a unique database collection.
    """
    # Create or connect to your local vector database
    vector_db = Chroma(
        persist_directory="./my_vector_db", 
        embedding_function=embeddings, 
        collection_name=session_id
    )
    
    # Semantic splitter: Breaks by paragraphs \n\n, then sentences ., then spaces
    # This prevents cutting gene names or chemical formulas in half.
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
                
                # Create semantic chunks
                chunks = text_splitter.create_documents([full_text], metadatas=[{"source": filename}])
                
                # Save to database
                vector_db.add_documents(chunks)
                print(f"Indexed {len(chunks)} semantic chunks from {filename}")
            except Exception as e:
                print(f"Could not process {filename}: {e}")
    
    return f"Successfully indexed into session: {session_id}"

def ask_agent(query, session_id):
    """
    Retrieves the most relevant biological context and uses the Qwen3 
    LLM to synthesize a scientifically accurate answer.
    """
    vector_db = Chroma(
        persist_directory="./my_vector_db", 
        embedding_function=embeddings, 
        collection_name=session_id
    )
    
    # Retrieve the 4 most relevant chunks from the papers
    docs = vector_db.similarity_search(query, k=4)
    context_text = "\n\n".join([doc.page_content for doc in docs])
    
    # Prompt the LLM
    prompt = f"""
    You are an expert biology research assistant. 
    Use the provided research context to answer the question.
    If the answer is not in the context, state that you don't have enough information.
    
    Context:
    {context_text}
    
    Question: 
    {query}
    """
    
    response = llm.invoke(prompt)
    return response.content