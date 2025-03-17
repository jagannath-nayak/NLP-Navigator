import streamlit as st
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util

st.title("Text Analysis Suite 📝🔍")
st.write("Perform text summarization, processing, and similarity comparison.")

# Load Summarization Model
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Load Similarity Model
@st.cache_resource
def load_similarity_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

summarizer = load_summarizer()
similarity_model = load_similarity_model()

# Text Summarization
st.header("Text Summarization")
user_text = st.text_area("Enter text to summarize:")
if st.button("Summarize"):
    if user_text:
        summary = summarizer(user_text, max_length=50, min_length=25, do_sample=False)
        st.write("### Summary:")
        st.success(summary[0]['summary_text'])
    else:
        st.warning("Please enter some text to summarize.")

# Text Processing
st.header("Text Processing")
nltk.download('stopwords')
remove_stop_words_option = st.checkbox("Remove Stop Words")
stemming_option = st.checkbox("Apply Stemming")

def remove_stop_words(text):
    stop_words = set(stopwords.words('english'))
    words = text.split()
    return ' '.join([word for word in words if word.lower() not in stop_words])

def stem_text(text):
    ps = PorterStemmer()
    words = text.split()
    return ' '.join([ps.stem(word) for word in words])

if user_text:
    processed_text = user_text
    if remove_stop_words_option:
        processed_text = remove_stop_words(processed_text)
    if stemming_option:
        processed_text = stem_text(processed_text)
    st.write("### Processed Text:", processed_text)

# Text Similarity
st.header("Text Similarity")
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
