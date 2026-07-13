import streamlit as st
import engine
import os

# --- Branding & Page Config ---
st.set_page_config(page_title="RacXo Agent", page_icon="🧬", layout="wide")
st.logo(":material/science:") 

st.title("🧬 RacXo Agent")
st.caption("Advanced RAG-powered Biology Intelligence Platform")
st.markdown("---")

# Session state initialization
if "session_id" not in st.session_state:
    st.session_state.session_id = "racxo_test_session_001"
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar ---
with st.sidebar:
    st.header("Research Workspace")
    st.info("Upload your papers to begin synthesis.")
    
    uploaded_files = st.file_uploader("Select PDF Research Papers", accept_multiple_files=True, type="pdf")
    
    if st.button("Index Documents", key="index_btn", use_container_width=True):
        if uploaded_files:
            if len(uploaded_files) > 5:
                st.error("Maximum 5 files allowed.")
            else:
                with st.spinner("Processing documents..."):
                    status = engine.process_and_index_pdfs_temporary(uploaded_files, st.session_state.session_id)
                    st.success(status)
                    st.session_state.indexed = True 
        else:
            st.warning("No files selected.")
            
    st.divider()
    
    # New Expander for professional documentation
    with st.expander("ℹ️ About Synthesis Research"):
        st.write("""
        The **Synthesize Research** tool provides:
        - **Multi-Source Mapping**: Synthesizes cross-document biological themes.
        - **Technical Decomposition**: Extracts core mechanisms, not just metadata.
        - **Researcher Attribution**: Links key findings to study authors.
        """)
        
    synthesize_clicked = st.button("Synthesize Research", key="synth_btn", type="primary", use_container_width=True)

# --- Main App Area ---
if synthesize_clicked:
    if "indexed" not in st.session_state:
        st.warning("⚠️ Please index your research papers before starting synthesis.")
    else:
        with st.container(border=True):
            st.subheader("📊 Research Synthesis Report")
            with st.spinner("RacXo is deep-diving into your research library..."):
                report = engine.synthesize_research(st.session_state.session_id)
                st.markdown(report)

# --- Chat Interface ---
st.subheader("💬 Chat with Research")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about the biological mechanisms..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🧬"):
        with st.spinner("Analyzing data..."):
            try:
                response = engine.ask_agent(prompt, st.session_state.session_id)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Analysis Error: {e}")