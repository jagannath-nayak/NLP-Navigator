import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.title("Word Cloud Generator ☁️")
st.write("Visualize the most frequent words in your text.")

# Input text
user_text = st.text_area("Enter text to generate a word cloud:")

if st.button("Generate Word Cloud"):
    if user_text:
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(user_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt)
    else:
        st.warning("Please enter some text to generate a word cloud.")
