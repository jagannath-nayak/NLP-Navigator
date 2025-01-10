import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline 
    
# Load sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

st.title("Sentiment Trends 📈")
st.write("Visualize sentiment trends over time.")

# Upload a dataset
uploaded_file = st.file_uploader("Upload a CSV file with 'Date' and 'Text' columns")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.write(df.head())

    # Apply sentiment analysis
    df['Sentiment'] = df['Text'].apply(lambda x: sentiment_pipeline(x)[0]['score'])

    # Plot sentiment trends
    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'], df['Sentiment'], marker='o', label='Sentiment Score')
    plt.title("Sentiment Over Time")
    plt.xlabel("Date")
    plt.ylabel("Sentiment Score")
    plt.legend()
    plt.grid()
    st.pyplot(plt)
