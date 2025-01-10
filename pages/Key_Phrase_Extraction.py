import streamlit as st
from keybert import KeyBERT

st.title("Key Phrase Extraction 🏷️")
st.write("Extract the most important phrases from your text.")

# Load KeyBERT model
@st.cache_resource
def load_keybert_model():
    return KeyBERT("all-MiniLM-L6-v2")

keybert_model = load_keybert_model()

# Input text
user_text = st.text_area("Enter text for key phrase extraction:")

# Number of key phrases to extract
num_phrases = st.slider("Number of Key Phrases", min_value=1, max_value=10, value=5)

if st.button("Extract Key Phrases"):
    if user_text:
        try:
            # Extract key phrases
            key_phrases = keybert_model.extract_keywords(user_text, keyphrase_ngram_range=(1, 2), stop_words="english", top_n=num_phrases)
            st.write("### Extracted Key Phrases:")
            for phrase, score in key_phrases:
                st.write(f"- *{phrase}* (Relevance: {score:.2f})")
        except Exception as e:
            st.error("An error occurred while extracting key phrases.")
            st.error(str(e))
    else:
        st.warning("Please enter some text for key phrase extraction.")