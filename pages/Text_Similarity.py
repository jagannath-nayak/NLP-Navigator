import streamlit as st
from sentence_transformers import SentenceTransformer, util

st.title("Text Similarity 🔗")
st.write("Compare the semantic similarity between two texts.")

# Load similarity model
@st.cache_resource
def load_similarity_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

similarity_model = load_similarity_model()

# Input texts
text1 = st.text_area("Enter the first text:")
text2 = st.text_area("Enter the second text:")

if st.button("Check Similarity"):
    if text1 and text2:
        embeddings1 = similarity_model.encode(text1, convert_to_tensor=True)
        embeddings2 = similarity_model.encode(text2, convert_to_tensor=True)
        similarity_score = util.pytorch_cos_sim(embeddings1, embeddings2).item()
        st.write(f"Semantic Similarity Score: **{similarity_score:.2f}**")
    else:
        st.warning("Please enter both texts for comparison.")
