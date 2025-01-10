import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download stopwords
nltk.download('stopwords')

# Text processing functions
def remove_stop_words(text):
    stop_words = set(stopwords.words('english'))
    words = text.split()
    filtered_text = ' '.join([word for word in words if word.lower() not in stop_words])
    return filtered_text

def stem_text(text):
    ps = PorterStemmer()
    words = text.split()
    stemmed_text = ' '.join([ps.stem(word) for word in words])
    return stemmed_text

# User input for text processing
st.header("Text Processing Options")
remove_stop_words_option = st.checkbox("Remove Stop Words")
stemming_option = st.checkbox("Apply Stemming")

user_text = st.text_area("Enter your text here:")

# Process the text based on user selections
if remove_stop_words_option:
    user_text = remove_stop_words(user_text)

if stemming_option:
    user_text = stem_text(user_text)

st.write("Processed Text:", user_text)