import streamlit as st
import engine
import uuid

# --- UI Setup ---
st.set_page_config(page_title="Biology Research Agent", layout="wide")
st.title("🧬 Biology Research Agent")
st.markdown("Upload your research papers and ask questions to get context-aware answers.")

# --- Session Management ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar: Document Ingestion ---
with st.sidebar:
    st.header("Upload Research Papers")
    uploaded_files = st.file_uploader("Select PDFs", accept_multiple_files=True, type="pdf")
    
    if st.button("Index Documents"):
        if uploaded_files:
            with st.spinner("Processing documents..."):
                # Uses the engine's temporary processing logic
                status = engine.process_and_index_pdfs_temporary(uploaded_files, st.session_state.session_id)
                st.success("Indexing complete!")
        else:
            st.warning("Please select files to index.")

# --- Chat Interface ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your research..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing research..."):
            response = engine.ask_agent(prompt, st.session_state.session_id)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})