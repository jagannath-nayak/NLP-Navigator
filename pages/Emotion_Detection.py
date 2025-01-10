import streamlit as st
from transformers import pipeline
import pandas as pd

st.title("Emotion Detection 😊")
st.write("Detect emotions in your text, such as joy, sadness, anger, and more.")

# Load emotion detection pipeline
@st.cache_resource
def load_emotion_model():
    return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

emotion_model = load_emotion_model()

# Input text
user_text = st.text_area("Enter text to detect emotions:")

# Detect Emotion Button
if st.button("Detect Emotion", key="detect_emotion"):
    if user_text:
        results = emotion_model(user_text)
        for result in results:
            st.write(f"Emotion: **{result['label']}**, Confidence: **{result['score']:.2f}**")
    else:
        st.warning("Please enter some text for emotion detection.")

# Feedback Section
if user_text:
    st.write("### Feedback Section")
    if st.button("Detect Emotion Again", key="detect_emotion_again"):
        results = emotion_model(user_text)
        for result in results:
            st.write(f"Emotion: **{result['label']}**, Confidence: **{result['score']:.2f}**")
    
    # User Feedback Mechanism
    rating = st.slider("Rate the accuracy of the analysis:", min_value=1, max_value=5, value=3, key="rating_slider")
    comment = st.text_area("Leave your comments or feedback:", key="comment_area")
    
    if st.button("Submit Feedback", key="submit_feedback"):
        def save_feedback(text, rating, comment):
            feedback_data = {'Text': [text], 'Rating': [rating], 'Comment': [comment]}
            df = pd.DataFrame(feedback_data)
            df.to_csv('user_feedback.csv', mode='a', header=False, index=False)
        
        save_feedback(user_text, rating, comment)
        st.success("Thank you for your feedback!")
else:
    st.warning("Please enter some text for emotion detection.")
