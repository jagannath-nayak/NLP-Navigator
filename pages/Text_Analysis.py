import streamlit as st
from transformers import pipeline

st.title("Text Analysis 📝")
st.write("Explore additional text analysis features, such as keyword extraction and summarization.")

# Summarization Feature
st.subheader("Summarize Text")

# Initialize summarizer pipeline safely
@st.cache_resource
def load_summarizer():
    try:
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        return summarizer
    except Exception as e:
        st.error("Failed to load summarization model. Check your internet connection or model settings.")
        st.stop()

summarizer = load_summarizer()

# Input text for summarization
user_text = st.text_area("Enter text to summarize:")

if st.button("Summarize"):
    if user_text:
        try:
            # Perform summarization
            summary = summarizer(user_text, max_length=50, min_length=25, do_sample=False)
            st.write("### Summary:")
            st.success(summary[0]['summary_text'])
        except Exception as e:
            st.error("An error occurred during summarization. Please try again.")
            st.error(str(e))
    else:
        st.warning("Please enter some text to summarize.")
