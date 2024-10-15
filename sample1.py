import os
import ssl
import nltk
import json
import streamlit as st
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Setting up SSL context for nltk
ssl._create_default_https_context = ssl._create_unverified_context

# Downloading punkt tokenizer
nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download('punkt')

# Load intents from a separate JSON file
def load_intents(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        intents = json.load(file)
    return intents

# Specify the path to the intents file
intents_file_path = "D:/Mridula/stud chatbot/stupid/intents.json"  # Update this with the actual path
intents = load_intents(intents_file_path)

# Create the vectorizer and classifier
vectorizer = TfidfVectorizer()
clf = LogisticRegression(random_state=0, max_iter=10000)

# Preprocess the data
tags = []
patterns = []
for intent in intents['intents']:
    for pattern in intent['patterns']:
        tags.append(intent['tag'])
        patterns.append(pattern)

# Training the model
x = vectorizer.fit_transform(patterns)
y = tags
clf.fit(x, y)

# Define the chatbot function
def chatbot(input_text):
    input_text = vectorizer.transform([input_text])
    tag = clf.predict(input_text)[0]
    for intent in intents['intents']:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            return response

# Streamlit UI
def main():
    # Custom CSS for chat bubbles
    st.markdown("""
    <style>
    .chat-wrapper {
        background-color: #f7f7f7;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 20px;
    }
    .user-message, .bot-message {
        margin: 10px;
        padding: 15px;
        border-radius: 10px;
        width: fit-content;
        max-width: 70%;
    }
    .user-message {
        background-color: #d4f0ff;
        align-self: flex-start;
    }
    .bot-message {
        background-color: #4db8ff;
        align-self: flex-end;
        color: white;
    }
    .message-container {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }
    .container {
        display: flex;
        flex-direction: column;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Chatbot")

    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # Input box for user messages
    user_input = st.text_input("Type your message", "")

    # Store user message in chat history
    if user_input:
        st.session_state['chat_history'].append(("user", user_input))
        response = chatbot(user_input)
        st.session_state['chat_history'].append(("bot", response))

    # Display chat history
    chat_display = st.container()
    with chat_display:
        for sender, message in st.session_state['chat_history']:
            if sender == "user":
                st.markdown(f"<div class='chat-wrapper message-container'><div class='user-message'>{message}</div></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-wrapper message-container'><div class='bot-message'>{message}</div></div>", unsafe_allow_html=True)

    if user_input and response.lower() in ['goodbye', 'bye']:
        st.write("Thank you for chatting with me. Have a great day!")
        st.stop()

if __name__ == '__main__':
    main()
