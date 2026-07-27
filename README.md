🧬 RacXo Agent
An AI-Powered Biological Research Assistant using Retrieval-Augmented Generation (RAG).

RacXo Agent is a full-stack RAG application designed to help researchers seamlessly index, analyze, and synthesize complex scientific literature. By leveraging vector databases and advanced LLM prompting, RacXo goes beyond simple summarization to extract core biological mechanisms, map cross-document themes, and provide accurate, source-cited answers to user queries.

🚀 Features
Multi-Document Ingestion: Upload up to 5 PDF research papers simultaneously.

Vector-Based Retrieval (RAG): Automatically parses, chunks, and indexes documents using ChromaDB for highly accurate contextual retrieval.

Structured Synthesis Engine: Generates a comprehensive research report that breaks down key findings, technical challenges, and notable researchers per individual source file.

Interactive Chat Interface: Ask complex, domain-specific questions about the uploaded literature, with the AI answering strictly based on the provided context.

Secure Cloud Deployment: Configured for safe, private hosting via Streamlit Community Cloud.

🛠️ Tech Stack
Frontend: Streamlit (Python)

Backend Framework: LangChain

Vector Database: ChromaDB

Document Processing: PyPDF, LangChain Text Splitters

Embeddings & LLM: [Qwen3:14b and nomic-embed-text:latest]

💻 Local Installation & Setup
Clone the repository:

Bash
git clone https://github.com/yourusername/racxo-agent.git
cd racxo-agent
Install dependencies:
Ensure you have Python installed, then run:

Bash
pip install -r requirements.txt
Set up environment variables:
If using API keys (e.g., OpenAI), create a .streamlit/secrets.toml file in the root directory and add your keys securely:

Ini, TOML
OPENAI_API_KEY = "your-api-key-here"
Run the application:

Bash
streamlit run app.py
🧠 How It Works
Upload: Users upload PDF documents via the sidebar.

Index: The app chunks the text and stores the embeddings in a local, ephemeral ChromaDB instance.

Synthesize: The agent iterates through the metadata to generate a structured report detailing the findings of each unique paper.

Chat: The user can query the agent, which retrieves the most relevant chunks from the vector database to construct an accurate response.

🗺️ Future Roadmap
This project currently serves as a foundational RAG prototype. Future iterations will focus on transitioning to production-grade architecture, including:

Agentic RAG: Implementing tool-use, self-correction, and planning capabilities.

Loop Engineering: Refining how the agent iteratively searches and evaluates information before answering.

Advanced Frontend UI: Enhancing the Streamlit interface for a crisper, more dynamic user experience.

Created by [Rachit Chilumuru}

linkedin.com/in/rachit-chilumuru-058311397
