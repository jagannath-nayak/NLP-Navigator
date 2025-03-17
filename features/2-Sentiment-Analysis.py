import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline

st.title("Sentiment Analysis: Comparison & Trends ⚖️📈")
st.write("Compare sentiments between texts and visualize sentiment trends over time.")

# Load sentiment analysis model
@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis")

sentiment_model = load_sentiment_model()

# Sentiment Comparison Section
st.header("Sentiment Comparison")
st.write("Compare the sentiments of two texts.")

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

# Sentiment Trends Section
st.header("Sentiment Trends")
st.write("Visualize sentiment trends over time.")

uploaded_file = st.file_uploader("Upload a CSV file with 'Date' and 'Text' columns")
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.write(df.head())

        if 'Text' not in df.columns or 'Date' not in df.columns:
            st.error("The uploaded file must have 'Date' and 'Text' columns.")
        else:
            df['Sentiment'] = df['Text'].apply(lambda x: sentiment_model(x)[0]['score'])
            
            # Plot sentiment trends
            plt.figure(figsize=(10, 5))
            plt.plot(df['Date'], df['Sentiment'], marker='o', label='Sentiment Score')
            plt.title("Sentiment Over Time")
            plt.xlabel("Date")
            plt.ylabel("Sentiment Score")
            plt.legend()
            plt.grid()
            st.pyplot(plt)
    except Exception as e:
        st.error(f"An error occurred: {e}")
