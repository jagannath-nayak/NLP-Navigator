import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from transformers.pipelines import pipeline  
import numpy as np
import nltk
import os
from nltk.tokenize import sent_tokenize, word_tokenize

# ✅ Correct NLTK tokenizer handling
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

st.title("📊 Sentiment Heatmap & Trends")

# ✅ Load sentiment model (cached for better performance)
@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis")

sentiment_model = load_sentiment_model()

# ✅ Function to get sentiment scores
def get_sentiment_scores(text):
    """Returns a sentiment score based on the input text."""
    if not text.strip():
        return 0  # Return neutral score if text is empty
    
    sentiment_result = sentiment_model(text)[0]
    label = sentiment_result['label']
    score = sentiment_result['score']
    
    if label == "POSITIVE":
        return score  # Positive values
    elif label == "NEGATIVE":
        return -score  # Negative values
    else:
        return 0  # Neutral values

# ✅ Heatmap color selection
heatmap_colors = {
    "Red-Yellow-Green": "RdYlGn",
    "Cool (Blue-Purple)": "coolwarm",
    "Magma (Dark Theme)": "magma",
    "Plasma (High Contrast)": "plasma"
}
selected_color = st.selectbox("🎨 Choose Heatmap Color Theme:", list(heatmap_colors.keys()))

# ✅ File upload or manual text input
st.subheader("📂 Upload a CSV/Text file or enter text:")
uploaded_file = st.file_uploader("Upload a `.txt` or `.csv` file", type=["txt", "csv"])

user_text = ""
df = None  # Initialize df to prevent reference errors

if uploaded_file:
    if uploaded_file.name.endswith(".txt"):
        user_text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

        # ✅ Validate CSV columns
        if "Date" in df.columns and "Text" in df.columns:
            df = df.dropna(subset=["Text"])  # Remove empty rows
            st.write("✅ CSV detected with Date & Text columns.")
        else:
            st.error("❌ CSV must contain 'Date' and 'Text' columns.")
            st.stop()
else:
    user_text = st.text_area("✏️ Or enter text manually:", height=200)

# ✅ Select analysis level
analysis_level = st.radio("🔍 Select Analysis Level:", ["Sentence-Level", "Word-Level"])

if st.button("🚀 Generate Heatmap"):
    if uploaded_file and uploaded_file.name.endswith(".csv"):
        # 📅 Sentiment Over Time
        df["Sentiment Score"] = df["Text"].apply(get_sentiment_scores)
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")

        # ✅ Handle case where all text is empty
        if df["Sentiment Score"].isnull().all():
            st.error("❌ No valid text found in the CSV file for sentiment analysis.")
        else:
            # Plot time-series sentiment
            plt.figure(figsize=(10, 5))
            plt.plot(df["Date"], df["Sentiment Score"], marker="o", linestyle="-", color="b")
            plt.axhline(y=0, color="gray", linestyle="--")
            plt.title("📅 Sentiment Trend Over Time")
            plt.xlabel("Date")
            plt.ylabel("Sentiment Score")
            plt.xticks(rotation=45)
            plt.grid()
            st.pyplot(plt)

    elif user_text.strip():
        # ✅ Process Sentences or Words
        text_segments = sent_tokenize(user_text) if analysis_level == "Sentence-Level" else word_tokenize(user_text)

        if not text_segments:
            st.error("❌ No valid text entered for sentiment analysis.")
        else:
            # ✅ Get sentiment scores
            sentiment_scores = [get_sentiment_scores(segment) for segment in text_segments]

            # ✅ Normalize for heatmap
            norm_scores = np.array(sentiment_scores).reshape(1, -1)

            # ✅ Plot heatmap
            plt.figure(figsize=(max(10, len(sentiment_scores) // 2), 1))
            sns.heatmap(norm_scores, annot=True, fmt=".2f", cmap=heatmap_colors[selected_color], center=0, linewidths=1, xticklabels=False)
            plt.title("📊 Sentiment Heatmap")
            st.pyplot(plt)

    else:
        st.warning("⚠️ Please upload a text file, CSV file, or enter text before generating the heatmap.")
