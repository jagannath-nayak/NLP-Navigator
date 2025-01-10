import streamlit as st
from streamlit_lottie import st_lottie
import requests

# Theme selection
theme = st.selectbox("Select Theme:", ["Light", "Dark"])

if theme == "Dark":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #2E2E2E;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: white;
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to load Lottie animations
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        st.warning("Failed to load animation.")
        return None
    return r.json()

# Load a Lottie animation
lottie_animation = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_x62chJ.json")

# Main Page
st.title("NLP Navigator Application")
st.write("Welcome to the NLP Navigator App! The app uses natural language processing to navigate through text data.")

# Sidebar Navigation
st.sidebar.title("Navigation")
st.sidebar.write("Use the sidebar to navigate through the app pages:")

# Display Lottie animation on the main page
st_lottie(lottie_animation, speed=1, width=700, height=700, key="animation")

st.write(
    """
    **Features:**  
    - **Sentiment Trends:** Analyze sentiment trends over time.  
    - **Text Analysis:** Perform advanced text analysis like summarization.
    - **Emotion Detection:** Detect emotions such as joy, sadness, anger, etc., in text using a Hugging Face model.
    - **Word Cloud Generator:** Generate a word cloud from user-provided text.
    - **Sentiment Comparison:** Compare sentiments of two different texts side by side.
    - **Text Similarity:** Check the semantic similarity between two texts.
    - **Key Phrase Extraction:** Extract key phrases from the given text using NLP. 
    - **Text Processing:** Provide options for text preprocessing (e.g., removing stop words, stemming) before analysis.
    """
)
st.sidebar.write("Visit each page for detailed features.")
