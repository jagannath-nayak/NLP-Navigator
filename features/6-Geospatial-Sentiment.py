import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from transformers.pipelines import pipeline  
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

st.title("📍 Geospatial Sentiment Mapping")

# ✅ Load Sentiment Model (Cached)
@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis")

sentiment_model = load_sentiment_model()

# ✅ Function to Get Sentiment Scores
def get_sentiment_scores(text):
    """Returns sentiment score from text."""
    sentiment_result = sentiment_model(text)[0]
    label = sentiment_result['label']
    score = sentiment_result['score']
    
    return score if label == "POSITIVE" else -score if label == "NEGATIVE" else 0

# ✅ Convert Location to Latitude & Longitude
geolocator = Nominatim(user_agent="geo-sentiment")

@st.cache_data
def get_lat_lon(location):
    """Fetches latitude & longitude for a given location."""
    try:
        time.sleep(1)  # Prevents API rate limit errors
        location_data = geolocator.geocode(location, timeout=10)
        return (location_data.latitude, location_data.longitude) if location_data else (None, None)
    except GeocoderTimedOut:
        return (None, None)

# ✅ File Upload Section
st.subheader("📂 Upload a CSV File with 'Location' & 'Text' Columns")
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # ✅ Validate CSV Columns
    if "Location" in df.columns and "Text" in df.columns:
        df = df.dropna(subset=["Location", "Text"])  # Remove Empty Rows
        st.write("✅ CSV Detected with Location & Text Columns.")

        # ✅ Perform Sentiment Analysis
        df["Sentiment Score"] = df["Text"].apply(get_sentiment_scores)

        # ✅ Get Latitude & Longitude for Each Location
        df["Coordinates"] = df["Location"].apply(lambda loc: get_lat_lon(loc))

        # ✅ Filter Out Locations That Failed Geocoding
        df = df[df["Coordinates"].notnull()]

        # ✅ Create Map
        sentiment_map = folium.Map(location=[20, 0], zoom_start=2)

        # ✅ Add Marker Clusters
        marker_cluster = MarkerCluster().add_to(sentiment_map)

        for _, row in df.iterrows():
            lat, lon = row["Coordinates"]
            sentiment = row["Sentiment Score"]
            color = "green" if sentiment > 0 else "red" if sentiment < 0 else "orange"

            folium.Marker(
                location=[lat, lon],
                popup=f"{row['Location']}\nSentiment Score: {sentiment:.2f}",
                icon=folium.Icon(color=color),
            ).add_to(marker_cluster)

        # ✅ Display Map
        folium_static(sentiment_map)

    else:
        st.error("❌ CSV must contain 'Location' and 'Text' columns.")
