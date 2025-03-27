import requests
import streamlit as st

# Retrieve API credentials from secrets.toml
token = st.secrets["api"]["key"]
base_url = st.secrets["api"]["base_url"]

# Streamlit Page Config
st.set_page_config(page_title="AI-powered Q&A", layout="centered")

# Page Title & Description
st.title("🤖 AI-powered Q&A with RAGie")
st.write("Ask any question, and RAGie AI will retrieve the most relevant answer from its knowledge base.")

# Sidebar Configuration
st.sidebar.header("🔧 Settings")
top_k = st.sidebar.slider("Top K", min_value=1, max_value=30, value=2)
max_chunks_per_document = st.sidebar.slider("Max Chunks per document", min_value=1, max_value=5, value=2)
rerank = st.sidebar.checkbox("Enable Re-Ranking", value=False)
recency_bias = st.sidebar.checkbox("Enable Recency Bias", value=False)

# User Input Section
question = st.text_input("Enter your question:", placeholder="e.g., How often does Redbrain share updates?", key="user_question")

# Automatically trigger on Enter
if question:
    st.session_state["trigger"] = True

if st.session_state.get("trigger", False) or st.button("Get Answer"):
    if not question:
        st.warning("Please enter a question.")
    else:
        url = f"{base_url}/retrievals"
        payload = {
            "query": question,
            "top_k": top_k,
            "rerank": rerank,
            "recency_bias": recency_bias,
            "max_chunks_per_document": max_chunks_per_document
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {token}"
        }

        with st.spinner("Fetching response... Please wait."):
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                result = response.json()
                scored_chunks = result.get("scored_chunks", [])
                answer = scored_chunks[0].get("text", "No relevant answer found.") if scored_chunks else "No relevant answer found."

                st.success("Answer Retrieved!")
                st.write(answer)
            else:
                st.error("Failed to retrieve answer. Please try again later.")
                st.write(f"Error: {response.text}")

    st.session_state["trigger"] = False
