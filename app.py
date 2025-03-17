import streamlit as st
st.set_page_config(page_title="NLP NAVIGATOR", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

from features.auth import authentication
from features.functions import load_lottie_file
import streamlit_lottie as st_lottie

# Initialize session state variables
if 'register' not in st.session_state:
    st.session_state['register'] = False
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {}

def intro():
    st.header("NLP NAVIGATOR : Represents AI and NLP capabilities 🧠 ", divider='rainbow')
    
    with st.container(border=True):
        left_col, right_col = st.columns(2)
        with left_col:
                st.subheader("About NLP NAVIGATOR", divider='rainbow')
                intro = '''🚀 Welcome to NLP Navigator!
                An AI-powered text analysis toolkit for unlocking insights from language. 
                Whether you're analyzing sentiments, summarizing documents, extracting key phrases, 
                or comparing text similarity and Unlock insights from language with cutting-edge NLP models.
                '''
                st.markdown(intro)

        with right_col:
                robot_assist = load_lottie_file("animations/banner.json")
                st_lottie.st_lottie(robot_assist, loop=True, width=500, height=500)
                
    with st.container(border=True):
            left_col, right_col = st.columns(2)
            with right_col:
                st.subheader("Features of NLP NAVIGATOR ℹ️", divider='rainbow')
                features = [
                    "**Text Processing & Cleaning ** Remove stop words, apply stemming, and prepare text for analysis.",
                    "**Sentiment & Emotion Analysis:** Detect emotions and sentiments in text.",
                    "**Key Phrase Extraction & Summarization** Identify important phrases and generate concise summaries.",
                    "**Text Similarity & Comparison:** Compare different texts and measure their semantic similarity.",
                    "**Feedback:** Feedback feature allows users to share their experience and suggestions for improvement."
                ]
                for feature in features:
                    st.markdown(f"🔹 {feature}")
                st.write("*Explore the features from the sidebar navigation.*")

            with left_col:
                feature_animation = load_lottie_file("animations/loading.json")
                st_lottie.st_lottie(feature_animation, loop=True, width=500, height=400)

    with st.container(border=True):
            st.subheader("Why SpamDefender.AI? 🚀", divider='rainbow')
            left_col, right_col = st.columns(2)
            with left_col:
                benefits = [
                    "Enhanced Text Understanding 🧠 - Detect emotions & sentiment in text (joy, sadness, anger, etc.)Compare text similarity and analyze context effectively.",
                    "Time-Saving Automation ⏳- Unlike most spam filters that focus only on emails, SpamDefender AI protects both text messages and emails.",
                    "Feedback Loop - Allows users to provide feedback on the accuracy of nlp navigator system.",
                    "Data-Driven Insights 📊- Analyze trends in sentiment over time for better decision-making. Identify patterns in text to optimize content strategies.",
                    "Smart NLP Processing 🔍 - Clean and preprocess text by removing stop words & applying stemming. Use AI-powered models for key phrase extraction and summarization."
                ]
                for benefit in benefits:
                    st.markdown(f"🔹 {benefit}")

            with right_col:
                benefits_animation = load_lottie_file("animations/success.json")
                st_lottie.st_lottie(benefits_animation, loop=True, width=500, height=300)

    with st.container(border=True):
            st.subheader("FAQs❓", divider='rainbow')
            # FAQ 1
            with st.expander("What is NLP Navigator?"):
                st.write("NLP Navigator is an AI-powered text analysis toolkit that helps users analyze sentiment, extract key phrases, summarize text, compare similarity, and process text efficiently.")
            # FAQ 2
            with st.expander("How does sentiment analysis work?"):
                st.write("NLP Navigator uses transformer-based AI models to classify text as positive, negative, or neutral, along with confidence scores.")
            #FAQ 3
            with st.expander("Can I analyze multiple texts at once?"):
                st.write("Yes! NLP Navigator supports batch processing for analyzing multiple texts simultaneously.")
            # FAQ 4
            with st.expander("Do I need coding knowledge to use NLP Navigator?"):
                st.write("No! NLP Navigator has a simple and user-friendly Streamlit interface, making it accessible to everyone, even without coding skills.")

# Run authentication system
authentication()

if st.session_state["authentication_status"]:
    pg = st.navigation([
    st.Page(title="Home", page = intro, icon="🏠"),
    st.Page(title="Emotion Keyphrase",page="features/1-Emotion-Keyphrase.py", icon="🔑"),
    st.Page(title="Sentiment Analysis",page="features/2-Sentiment-Analysis.py", icon="📝"),
    st.Page(title="Text Analysis",page="features/3-Text-Analysis-Tools.py", icon = "🛠"),
    st.Page(title="Word Cloud",page="features/4-Word-Cloud.py", icon="☁️"),
    st.Page(title="Feedback",page="features/5-Feedback.py", icon="💬")
      ])
    pg.run()
