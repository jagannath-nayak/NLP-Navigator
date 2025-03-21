import streamlit as st
from transformers.pipelines import pipeline  
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
import pandas as pd

st.title("Emotion Detection & Key Phrase Extraction 😊🏷️")
st.write("Analyze your text for emotions and extract key phrases.")

# Load emotion detection model safely
@st.cache_resource
def load_emotion_model():
    try:
        return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
    except Exception as e:
        st.error("Error loading emotion detection model.")
        st.error(str(e))
        return None  # Prevent crashes

# Load KeyBERT model safely
@st.cache_resource
def load_keybert_model():
    try:
        return KeyBERT(SentenceTransformer("all-MiniLM-L6-v2"))
    except Exception as e:
        st.error("Error loading KeyBERT model.")
        st.error(str(e))
        return None

emotion_model = load_emotion_model()
keybert_model = load_keybert_model()

# Input text
user_text = st.text_area("Enter text for analysis:")

# Number of key phrases to extract
num_phrases = st.slider("Number of Key Phrases", min_value=1, max_value=10, value=5)

if st.button("Analyze Text"):
    if user_text.strip():  # Ensure input isn't empty
        if emotion_model:
            results = emotion_model(user_text.strip())
            st.write("### Emotion Analysis:")
            for result in results:
                st.write(f"Emotion: **{result['label']}**, Confidence: **{result['score']:.2f}**")

        # Key Phrase Extraction
        if keybert_model:
            try:
                key_phrases = keybert_model.extract_keywords(
                    user_text.strip(), keyphrase_ngram_range=(1, 2), stop_words="english", top_n=num_phrases
                )
                st.write("### Extracted Key Phrases:")
                for phrase, score in key_phrases:
                    st.write(f"- *{phrase}* (Relevance: {score:.2f})")
            except Exception as e:
                st.error("An error occurred while extracting key phrases.")
                st.code(str(e))
    else:
        st.warning("Please enter some text for analysis.")
