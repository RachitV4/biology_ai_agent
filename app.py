import streamlit as st
import engine
import uuid

# --- UI Setup ---
st.set_page_config(page_title="RacXo Agent", page_icon="🧬", layout="wide")

st.title("🧬 RacXo Agent")

# Initialize Session State
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar: Upload & Indexing ---
with st.sidebar:
    st.header("About RacXo")
    st.info("Your intelligent, RAG-powered biology research assistant.")
    st.divider()
    st.header("Upload Research")
    
    uploaded_files = st.file_uploader("Select PDFs", accept_multiple_files=True, type="pdf")
    
    if st.button("Index Documents"):
        if uploaded_files:
            with st.spinner("RacXo is indexing your papers..."):
                # Call the temporary processing function we defined in engine.py
                status = engine.process_and_index_pdfs_temporary(uploaded_files, st.session_state.session_id)
                st.success(status)
        else:
            st.warning("Please select files first.")

# --- Chat Interface ---
# Display historical messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("Ask RacXo a question..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # RacXo response
    with st.chat_message("assistant", avatar="🧬"):
        with st.spinner("RacXo is thinking..."):
            try:
                response = engine.ask_agent(prompt, st.session_state.session_id)
                st.markdown(response)
                # Store assistant response
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")