import streamlit as st
from transformers import pipeline
from keybert import KeyBERT
import pandas as pd

st.title("Emotion Detection & Key Phrase Extraction 😊🏷️")
st.write("Analyze your text for emotions and extract key phrases.")

# Load emotion detection model
@st.cache_resource
def load_emotion_model():
    return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

# Load KeyBERT model
@st.cache_resource
def load_keybert_model():
    return KeyBERT("all-MiniLM-L6-v2")

emotion_model = load_emotion_model()
keybert_model = load_keybert_model()

# Input text
user_text = st.text_area("Enter text for analysis:")

# Number of key phrases to extract
num_phrases = st.slider("Number of Key Phrases", min_value=1, max_value=10, value=5)

if st.button("Analyze Text"):
    if user_text:
        # Emotion Detection
        results = emotion_model(user_text)
        st.write("### Emotion Analysis:")
        for result in results:
            st.write(f"Emotion: **{result['label']}**, Confidence: **{result['score']:.2f}**")

        # Key Phrase Extraction
        try:
            key_phrases = keybert_model.extract_keywords(user_text, keyphrase_ngram_range=(1, 2), stop_words="english", top_n=num_phrases)
            st.write("### Extracted Key Phrases:")
            for phrase, score in key_phrases:
                st.write(f"- *{phrase}* (Relevance: {score:.2f})")
        except Exception as e:
            st.error("An error occurred while extracting key phrases.")
            st.error(str(e))
    else:
        st.warning("Please enter some text for analysis.")

# Feedback Section
if user_text:
    st.write("### Feedback Section")
    rating = st.slider("Rate the accuracy of the analysis:", min_value=1, max_value=5, value=3)
    comment = st.text_area("Leave your comments or feedback:")
    
    if st.button("Submit Feedback"):
        def save_feedback(text, rating, comment):
            feedback_data = {'Text': [text], 'Rating': [rating], 'Comment': [comment]}
            df = pd.DataFrame(feedback_data)
            df.to_csv('user_feedback.csv', mode='a', header=False, index=False)
        
        save_feedback(user_text, rating, comment)
        st.success("Thank you for your feedback!")
