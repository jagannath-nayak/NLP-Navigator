import streamlit as st
from transformers import pipeline

st.title("Sentiment Comparison ⚖️")
st.write("Compare the sentiments of two texts.")

# Load sentiment analysis pipeline
@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis")

sentiment_model = load_sentiment_model()

# Input texts
text1 = st.text_area("Enter the first text:")
text2 = st.text_area("Enter the second text:")

if st.button("Compare Sentiments"):
    if text1 and text2:
        result1 = sentiment_model(text1)[0]
        result2 = sentiment_model(text2)[0]
        st.write(f"Text 1 Sentiment: **{result1['label']}** (Confidence: {result1['score']:.2f})")
        st.write(f"Text 2 Sentiment: **{result2['label']}** (Confidence: {result2['score']:.2f})")
    else:
        st.warning("Please enter both texts for comparison.")
