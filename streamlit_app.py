import streamlit as st
from main import app  # Import LangGraph workflow

st.set_page_config(page_title="Deep Research Agent", layout="wide")
st.title("🧠 Deep Research AI Agent")

query = st.text_input("Ask your research question:")

if st.button("Generate Answer"):
    with st.spinner("🧠 Researching..."):
        result = app.invoke({"query": query})
        st.subheader("📄 Final Answer")
        st.write(result["final_answer"])