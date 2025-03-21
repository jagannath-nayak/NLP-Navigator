import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from streamlit_autorefresh import st_autorefresh  # ✅ Import for proper auto-refresh

# Load environment variables from .env file
load_dotenv()

# API Keys
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# ✅ Improved Sentiment Analysis Function
def get_sentiment(text):
    """Uses Hugging Face API + custom rule-based sentiment for IT news."""
    if not text or len(text) < 10:  
        return "Neutral"

    # Rule-Based Sentiment Boosting for IT Topics
    text_lower = text.lower()
    negative_keywords = ["vulnerability", "ransomware", "attack", "breach", "hacked", "phishing"]
    positive_keywords = ["secured", "patched", "protected", "encrypted", "defended", "firewall"]

    if any(word in text_lower for word in negative_keywords):
        return "NEGATIVE"
    if any(word in text_lower for word in positive_keywords):
        return "POSITIVE"

    # AI-Based Sentiment Analysis
    url = "https://api-inference.huggingface.co/models/SamLowe/roberta-base-go_emotions"
    headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
    payload = {"inputs": text}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            sentiments = response.json()
            if isinstance(sentiments, list) and len(sentiments) > 0:
                return max(sentiments[0], key=lambda x: x["score"])["label"]
        except KeyError:
            return "Neutral"
    return "Neutral"

# Function to fetch news articles using News API
def fetch_news(query):
    """Fetches news articles from NewsAPI."""
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("articles", [])
    return []

# Function to fetch web search results using Google Custom Search API
def fetch_web_results(query):
    """Fetches search results from Google Custom Search API."""
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={GOOGLE_CSE_ID}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("items", [])
    return []

# Function to analyze sentiment for news articles
def analyze_news_sentiment(articles):
    """Performs sentiment analysis on news articles using both title & description."""
    df = pd.DataFrame(articles)

    if "publishedAt" not in df.columns:
        st.error("Error: 'publishedAt' column missing in API response.")
        return pd.DataFrame()  # Return empty DataFrame

    # Convert and rename columns
    df.rename(columns={"publishedAt": "Published At", "title": "Title", "description": "Description", "url": "URL"}, inplace=True)
    df["Published At"] = pd.to_datetime(df["Published At"]).dt.date  # Convert to date format

    # Apply sentiment analysis to title + description (if available)
    df["Sentiment"] = df.apply(lambda row: get_sentiment(f"{row['Title']} {row['Description']}" if pd.notnull(row["Description"]) else row["Title"]), axis=1)

    return df[["Title", "Description", "Sentiment", "Published At", "URL"]]


# Function to perform trend forecasting
def forecast_trends(sentiment_df):
    """Uses Exponential Smoothing for forecasting sentiment trends."""
    if sentiment_df.empty:
        return pd.DataFrame()

    sentiment_df["Published At"] = pd.to_datetime(sentiment_df["Published At"])
    trend_data = sentiment_df.groupby(["Published At", "Sentiment"]).size().reset_index(name="count")

    forecast_results = []
    for sentiment in trend_data["Sentiment"].unique():
        temp_df = trend_data[trend_data["Sentiment"] == sentiment]
        if len(temp_df) < 3:  # Need at least 3 data points
            continue

        # Fit model
        model = ExponentialSmoothing(temp_df["count"], trend="add", seasonal=None)
        fit = model.fit()
        future_dates = [temp_df["Published At"].max() + timedelta(days=i) for i in range(1, 6)]
        predictions = fit.forecast(5)

        # Store results
        for date, pred in zip(future_dates, predictions):
            forecast_results.append({"Date": date, "Sentiment": sentiment, "Count": pred})

    return pd.DataFrame(forecast_results)

# Streamlit UI
st.title("📊 Social Media Sentiment Tracking & Forecasting Dashboard")

# User input for keyword search
query = st.text_input("Enter a topic or keyword to analyze:", "Artificial Intelligence")

# Fetch & analyze news on button click
if st.button("Analyze Sentiment"):
    with st.spinner("Fetching news and analyzing sentiment..."):
        articles = fetch_news(query)
        sentiment_df = analyze_news_sentiment(articles)

        if not sentiment_df.empty:
            st.subheader("📊 Sentiment Analysis of News Articles")
            
            # Pie chart for sentiment distribution
            fig = px.pie(sentiment_df, names="Sentiment", title="News Sentiment Distribution")
            st.plotly_chart(fig)

            # Display table
            st.dataframe(sentiment_df)

            # Trend Forecasting
            forecast_df = forecast_trends(sentiment_df)
            if not forecast_df.empty:
                st.subheader("🔮 Sentiment Trend Forecasting")
                fig_forecast = px.line(forecast_df, x="Date", y="Count", color="Sentiment",
                                       title="Sentiment Forecast Over Next 5 Days")
                st.plotly_chart(fig_forecast)

        # Web Search Results
        web_results = fetch_web_results(query)
        if web_results:
            st.subheader("🔍 Web Search Results")
            for result in web_results[:5]:
                st.markdown(f"🔗 [{result['title']}]({result['link']})")
                
# ✅ Fixed Auto-Refresh (No Infinite Loop)
st.sidebar.header("🔄 Auto-Refresh")
refresh = st.sidebar.checkbox("Enable Auto-Refresh")  # Toggle auto-refresh
update_interval = st.sidebar.slider("Update Interval (seconds)", 10, 300, 60)  # Refresh rate

# ✅ Use `st_autorefresh()` Instead of `time.sleep()`
if refresh:
    st_autorefresh(interval=update_interval * 1000, key="data_refresh")
