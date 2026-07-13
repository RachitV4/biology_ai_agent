import streamlit as st
import engine

# --- Branding & Page Config ---
# '🧬' emoji as tab icon
st.set_page_config(page_title="RacXo Agent", page_icon="🧬", layout="wide")

# Add a logo to the top left of the sidebar
# Make sure to have a logo.png in your folder, or use a material icon:
st.logo(":material/science:") 

st.title("🧬 RacXo Agent")
st.markdown("---")

# Session state initialization
if "session_id" not in st.session_state:
    st.session_state.session_id = "racxo_test_session_001"
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar ---
with st.sidebar:
    st.header("Research Workspace")
    st.info("Your intelligent, RAG-powered biology research assistant.")
    st.divider()
    
    # This remains inside the 'with st.sidebar' block
    uploaded_files = st.file_uploader("Upload Research Papers (Max 5)", accept_multiple_files=True, type="pdf")
    
    # This remains inside the 'with st.sidebar' block
    if st.button("Index Documents"):
        if uploaded_files:
            with st.spinner("RacXo is indexing..."):
                status = engine.process_and_index_pdfs_temporary(uploaded_files, st.session_state.session_id)
                st.success(status)
        else:
            st.warning("Please select files first.")
            
    # This button stays in the sidebar too
    synthesize_clicked = st.button("Synthesize Research")

# --- Main App Area (OUTSIDE the sidebar block) ---
# Notice there is NO indentation here
if synthesize_clicked:
    with st.spinner("RacXo is analyzing across all papers..."):
        report = engine.synthesize_research(st.session_state.session_id)
        st.markdown(report)

    # 5-file limit enforced
    uploaded_files = st.file_uploader(
        "Upload Research Papers (Max 5)", 
        accept_multiple_files=True, 
        type="pdf"
    )
    
    # Validation logic for the 5-file limit
    if uploaded_files and len(uploaded_files) > 5:
        st.error("Please upload no more than 5 files.")
    elif st.button("Index Documents"):
        if uploaded_files:
            with st.spinner("RacXo is indexing..."):
                status = engine.process_and_index_pdfs_temporary(uploaded_files, st.session_state.session_id)
                st.success(status)
        else:
            st.warning("Please select files first.")

# --- Chat Interface ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask RacXo a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🧬"):
        with st.spinner("RacXo is thinking..."):
            try:
                # Ensure engine.ask_agent is using k=10
                response = engine.ask_agent(prompt, st.session_state.session_id)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")